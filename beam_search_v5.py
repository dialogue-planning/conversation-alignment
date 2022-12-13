from cmath import log
from dataclasses import dataclass
from typing import List, Union, Dict
from hovor.rollout.rollout_core import HovorRollout
from hovor.rollout.graph_setup import BeamSearchGraphGenerator


@dataclass
class Action:
    name: str
    probability: float
    beam: int
    score: float

    def __lt__(self, other):
        return self.score > other.score


@dataclass
class Intent:
    name: str
    probability: float
    outcome: str
    beam: int
    score: float

    def __eq__(self, other):
        return (
            self.name == other.name
            and self.probability == other.probability
            and self.outcome == other.outcome
        )

    def __lt__(self, other):
        return self.score > other.score


@dataclass
class Beam:
    id: int
    last_action: Union[Action, None]
    last_intent: Union[Intent, None]
    rankings: List[Union[Action, Intent]]
    rollout: HovorRollout
    scores: list
    fallbacks: int


def _is_fallback(output: Union[Action, Intent]):
    return output.name == "fallback"


def _handle_message_actions(beams: List[Beam], graph_gen: BeamSearchGraphGenerator):
    for i in range(len(beams)):
        result = beams[i].rollout.update_if_message_action(
            beams[i].last_action.name
        )
        if result:
            intent = Intent(
                name=result["intent"],
                probability=result["confidence"],
                outcome=result["outcome"],
                beam=i,
                score=log(result["confidence"]) + beams[i].last_action.score,
            )
            beams[i].last_intent = intent
            beams[i].rankings.append(intent)
            graph_gen.create_nodes_highlight_k(
                {intent.name: round(intent.score.real, 4)},
                "lightgoldenrod1",
                beams[i].last_action.name,
                i,
                [intent.name],
            )


def _reconstruct_beam_w_output(beams: List[Beam], outputs: List[Union[Action, Intent]]):
    new_beams = []
    for i in range(len(outputs)):
        # beam that the output came from
        at_beam = outputs[i].beam
        fallbacks = beams[at_beam].fallbacks
        if isinstance(outputs[i], Action):
            last_action = outputs[i]
            last_intent = beams[at_beam].last_intent
        else:
            last_intent = outputs[i]
            last_action = beams[at_beam].last_action
            if _is_fallback(outputs[i]):
                fallbacks += 1
        # reset the output beam id to the new one we're creating
        outputs[i].beam = i
        new_beams.append(Beam(
            i,
            last_action,
            last_intent,
            beams[at_beam].rankings + [outputs[i]],
            beams[at_beam].rollout.copy(),
            beams[at_beam].scores + [log(outputs[i].probability)],
            fallbacks
        ))
    return new_beams


def beam_search(k, max_fallbacks, conversation, output_files_path, filename):
    graph_gen = BeamSearchGraphGenerator(k)
    start_rollout = HovorRollout(output_files_path)
    starting_values = start_rollout.get_action_confidences(conversation[0])
    outputs = [
        Action(key, val, index, log(val))
        for index, (key, val) in enumerate(starting_values.items())
    ]
    # if there are less starting actions than there are beams, duplicate the best action until we reach k
    while len(outputs) < k:
        outputs.append(outputs[0])

    beams = []
    for beam in range(k):
        # create the initial beams
        beams.append(
            Beam(
                beam,
                outputs[beam],
                None,
                [outputs[beam]],
                HovorRollout(output_files_path),
                [log(outputs[beam].probability)],
                0
            )
        )
        # add the k actions to the graph
        graph_gen.create_nodes_highlight_k(
            {outputs[beam].name: round(outputs[beam].score.real, 4)},
            "skyblue",
            "START",
            beam,
            [outputs[beam].name],
        )
    _handle_message_actions(beams, graph_gen)
    # add the (total actions - k) nodes that won't be picked to the graph
    graph_gen.create_from_parent(
        {action.name: round(action.score.real, 4) for action in outputs[k:]},
        "skyblue",
    )
    for utterance in conversation[1:]:
        user = "USER" in utterance
        outputs = []
        for beam in range(len(beams)):
            if user:
                all_intent_confs = beams[beam].rollout.get_highest_intents(
                    beams[beam].last_action.name, utterance
                )
                for intent_cfg in all_intent_confs:
                    # find the score by taking the sum of the current beam thread which should be a list of log(prob)
                    outputs.append(
                        Intent(
                            intent_cfg["intent"],
                            intent_cfg["confidence"],
                            intent_cfg["outcome"],
                            beam,
                            (
                                sum(beams[beam].scores)
                                + log(intent_cfg["confidence"])
                            ).real,
                        )
                    )
            else:
                all_act_confs = beams[beam].rollout.get_action_confidences(
                    utterance,
                    beams[beam].last_action.name,
                    beams[beam].last_intent.name,
                    beams[beam].last_intent.outcome,
                )
                for act, conf in all_act_confs.items():
                    outputs.append(
                        Action(
                            act,
                            conf,
                            beam,
                            (sum(beams[beam].scores) + log(conf)).real,
                        )
                    )
        # sort the new list keeping track of each thread instead of the outputs
        outputs.sort()
        all_outputs = outputs
        outputs = outputs[0:k]

        node_color = "lightgoldenrod1" if user else "skyblue"
        graph_beam_chosen_map = {idx: [] for idx in range(k)}
        for output in outputs:
            graph_beam_chosen_map[output.beam].append(output.name)

        for beam, chosen in graph_beam_chosen_map.items():
            graph_gen.create_nodes_highlight_k(
                # filter ALL outputs by outputs belonging to the current beam
                # using the filtered outputs, map intents to probabilities to use in the graph
                {
                    output.name: round(output.score.real, 4)
                    for output in all_outputs
                    if output.beam == beam
                },
                node_color,
                beams[beam].rankings[-1].name,
                beam,
                chosen,
            )
        graph_gen.beams = [
            BeamSearchGraphGenerator.GraphBeam(
                {
                    k: v
                    for k, v in graph_gen.beams[
                        output.beam
                    ].parent_nodes_id_map.items()
                }
            )
            for output in outputs
        ]
        beams = _reconstruct_beam_w_output(beams, outputs)
        if user:
            for beam in beams:
                beam.rollout.update_state(
                    beam.last_action.name,
                    beam.last_intent.outcome,
                )
        else:
            _handle_message_actions(beams, graph_gen)

        for beam in beams:
            if beam.fallbacks >= max_fallbacks:
                beam.scores = [log(0.00000001)]

    for i in range(len(beams)):
        if beams[i].rollout.get_reached_goal():
            graph_gen.set_last_chosen(beams[i].rankings[-1].name, i)
            graph_gen.complete_conversation(
                round(beams[i].rankings[-1].score.real, 4)
            )
        head = "0"
        for elem in beams[i].rankings:
            tail = head
            # id must be > than the head to prevent referencing previous nodes with the same name
            head = graph_gen.beams[i].parent_nodes_id_map[elem.name].pop(0)
            while int(head) <= int(tail):
                head = graph_gen.beams[i].parent_nodes_id_map[elem.name].pop(0)
            graph_gen.graph.edge(
                tail, head, color="forestgreen", penwidth="10.0", arrowhead="normal"
            )
    graph_gen.graph.render(f"{filename}.gv", view=True)


if __name__ == "__main__":
    icaps_conversation_break_both = [
        {
            "HOVOR": "What invited talk do you want to see on Day 1? You can learn about Factored Transition Systems or the applications of Multi-Agent Path Finding."
        },
        {"USER": "beam want to see the talk on Factored Transition Systems."},
        {"HOVOR": "And then? What after the invited talk?"},
        {
            "USER": "beam want to learn more about classical planning and why applying heuristics is useful."
        },
        {
            "HOVOR": "What session do you want to see in the afternoon? Your options are: Model-Based Reasoning, Learning for Scheduling Applications, Search, and Optimal Planning."
        },
        {"USER": "Please schedule me in to watch the talk on Model-Based Reasoning."},
        {"HOVOR": "Thank you, enjoy your day!"},
    ]
    icaps_conversation_entity_drop = [
        {
            "HOVOR": "What invited talk do you want to see on Day 1? You can learn about Factored Transition Systems or the applications of Multi-Agent Path Finding."
        },
        {"USER": "beam want to see the talk on Factored Transition Systems."},
        {
            "HOVOR": "What session do you want to see in the morning? The sessions available are on Planning Representations and Scheduling, Verification, RL, or Heuristics in Classical Planning."
        },
        {
            "USER": "beam want to learn more about classical planning and why applying heuristics is useful."
        },
        {
            "HOVOR": "What session do you want to see in the afternoon? Your options are: Model-Based Reasoning, Learning for Scheduling Applications, Search, and Optimal Planning."
        },
        {"USER": "Please schedule me in to watch the talk on Model-Based Reasoning."},
        {"HOVOR": "Thank you, enjoy your day!"},
    ]
    # NOTE: FOR HOVORROLLOUT: RUN RASA MODEL BEFORE RUNNING
    output_dir = "C:\\Users\\Rebecca\\Desktop\\plan4dial\\plan4dial\\local_data\\rollout_no_system_icaps_bot_mini\\output_files"
    beam_search(
        3, 1, icaps_conversation_entity_drop, output_dir, "icaps_entity_drop_goal"
    )
    beam_search(
        3, 2, icaps_conversation_entity_drop, output_dir, "icaps_entity_drop_no_goal"
    )
    beam_search(3, 1, icaps_conversation_break_both, output_dir, "icaps_break_both")
