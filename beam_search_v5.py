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


def _new_beam_from_output(beams: List[Beam], output: Dict):
    at_beam = output.beam
    if isinstance(output, Action):
        last_action = output
        last_intent = beams[at_beam].last_intent
    else:
        last_intent = output
        last_action = beams[at_beam].last_action
    return Beam(
        at_beam,
        last_action,
        last_intent,
        beams[at_beam].rankings + [output],
        beams[at_beam].rollout.copy(),
        beams[at_beam].scores + [log(output.probability)],
    )


def beam_search(k, max_fallbacks, conversation, output_files_path, filename):
    beams = []
    graph_gen = BeamSearchGraphGenerator(k)
    for i in range(len(conversation)):
        if i == 0:
            start_rollout = HovorRollout(output_files_path)
            starting_values = start_rollout.get_action_confidences(conversation[i])
            outputs = [
                Action(key, val, index, log(val))
                for index, (key, val) in enumerate(starting_values.items())
            ]
            # if there are less starting actions than there are beams, duplicate the best action until we reach k
            while len(outputs) < k:
                outputs.append(outputs[0])
            for beam in range(k):
                beams.append(
                    Beam(
                        beam,
                        outputs[beam],
                        None,
                        [outputs[beam]],
                        HovorRollout(output_files_path),
                        [log(outputs[beam].probability)],
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
                # need in case of message actions at the beginning
                result = beams[beam].rollout.update_if_message_action(
                    beams[beam].last_action.name
                )
                if result:
                    intent = Intent(
                        name=result["intent"],
                        probability=result["confidence"],
                        outcome=result["outcome"],
                        beam=beam,
                        score=log(result["confidence"]) + beams[beam].last_action.score,
                    )
                    beams[beam].last_intent = intent
                    beams[beam].rankings.append(intent)
                    graph_gen.create_nodes_highlight_k(
                        {intent.name: round(intent.score.real, 4)},
                        "lightgoldenrod1",
                        beams[beam].last_action.name,
                        beam,
                        [intent.name],
                    )
            # add the (total actions - k) nodes that won't be picked to the graph
            graph_gen.create_from_parent(
                {action.name: round(action.score.real, 4) for action in outputs[k:]},
                "skyblue",
            )
        else:
            outputs = []
            for beam in range(k):
                if "USER" in conversation[i].keys():
                    all_intent_confs = beams[beam].rollout.get_highest_intents(
                        beams[beam].last_action.name, conversation[i]
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
                elif "HOVOR" in conversation[i].keys():
                    all_act_confs = beams[beam].rollout.get_action_confidences(
                        conversation[i],
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
            if "USER" in conversation[i].keys():
                # beam_holders = [[] for _ in range(k)]
                # list_intents = []
                # list_actions = []
                # list_rollout = []
                # list_scores = [[] for _ in range(k)]
                graph_beam_chosen_map = {idx: [] for idx in range(k)}
                # for idx in range(k):
                #     at_beam = outputs[idx].beam

                #     # setting up the next intents to add to the beam
                #     next_intent = outputs[idx]
                #     list_intents.append(next_intent)

                #     # carrying thrugh the proper last actions from previous beams
                #     list_actions.append(beams[at_beam].last_action)
                #     list_rollout.append(beams[at_beam].rollout)

                #     # keeping track of the old beam scores all unadded
                #     list_scores[idx].extend(beams[at_beam].scores)
                #     list_scores[idx].append(log(next_intent.probability))

                #     # setting the root of the current beam that will get additions
                #     beam_holders[idx].extend(beams[at_beam].rankings)
                #     beam_holders[idx].append(next_intent)

                #     graph_beam_chosen_map[at_beam].append(next_intent.name)
                for output in outputs:
                    graph_beam_chosen_map[output.beam].append(output.name)

                for beam, chosen_intents in graph_beam_chosen_map.items():
                    graph_gen.create_nodes_highlight_k(
                        # filter ALL outputs by outputs belonging to the current beam
                        # using the filtered outputs, map intents to probabilities to use in the graph
                        {
                            output.name: round(output.score.real, 4)
                            for output in all_outputs
                            if output.beam == beam
                        },
                        "lightgoldenrod1",
                        beams[beam].rankings[-1].name,
                        beam,
                        chosen_intents,
                    )
                # beams = []
                graph_beams_copy = graph_gen.beams
                graph_gen.beams = []
                beams = [_new_beam_from_output(beams, output) for output in outputs]
                for new_beam in range(k):
                    # beams.append(
                    #     Beam(
                    #         new_beam,
                    #         list_actions[new_beam],
                    #         list_intents[new_beam],
                    #         beam_holders[new_beam],
                    #         list_rollout[new_beam].copy(),
                    #         list_scores[new_beam],
                    #     )
                    # )
                    beams[new_beam].rollout.update_state(
                        beams[new_beam].last_action.name,
                        beams[new_beam].last_intent.outcome,
                    )
                    # also update the graph so they point to the right beams
                    # grab the old beam placement
                    # old_beam_placement = list_intents[new_beam].beam
                    old_beam_placement = beams[new_beam].last_intent.beam
                    graph_gen.beams.append(
                        BeamSearchGraphGenerator.GraphBeam(
                            {
                                k: v
                                for k, v in graph_beams_copy[
                                    old_beam_placement
                                ].parent_nodes_id_map.items()
                            }
                        )
                    )
            else:
                beam_holders = [[] for _ in range(k)]
                list_intents = []
                list_actions = []
                list_rollout = []
                list_scores = [[] for _ in range(k)]
                graph_beam_chosen_map = {idx: [] for idx in range(k)}
                for idx in range(k):
                    at_beam = outputs[idx].beam
                    # setting up the next actions to add to the beam
                    next_action = outputs[idx]
                    list_actions.append(next_action)
                    # carry through the last intents from the previous beams
                    list_intents.append(beams[at_beam].last_intent)

                    list_rollout.append(beams[at_beam].rollout)

                    list_scores[idx].extend(beams[at_beam].scores)
                    list_scores[idx].append(log(next_action.probability))

                    beam_holders[idx].extend(beams[at_beam].rankings)
                    beam_holders[idx].append(next_action)

                    graph_beam_chosen_map[at_beam].append(next_action.name)

                for beam, chosen_acts in graph_beam_chosen_map.items():
                    graph_gen.create_nodes_highlight_k(
                        {
                            output.name: round(output.score.real, 4)
                            for output in all_outputs
                            if output.beam == beam
                        },
                        "skyblue",
                        beams[beam].rankings[-1].name,
                        beam,
                        chosen_acts,
                    )

                beams = []
                graph_beams_copy = graph_gen.beams
                graph_gen.beams = []
                for new_beam in range(k):
                    beams.append(
                        Beam(
                            new_beam,
                            list_actions[new_beam],
                            list_intents[new_beam],
                            beam_holders[new_beam],
                            list_rollout[new_beam].copy(),
                            list_scores[new_beam],
                        )
                    )

                    # also update the graph so they point to the right beams
                    # grab the old beam placement
                    old_beam_placement = list_actions[new_beam].beam
                    graph_gen.beams.append(
                        BeamSearchGraphGenerator.GraphBeam(
                            {
                                k: v
                                for k, v in graph_beams_copy[
                                    old_beam_placement
                                ].parent_nodes_id_map.items()
                            }
                        )
                    )

                    result = beams[new_beam].rollout.update_if_message_action(
                        beams[new_beam].last_action.name
                    )
                    if result:
                        intent = Intent(
                            name=result["intent"],
                            probability=result["confidence"],
                            outcome=result["outcome"],
                            beam=new_beam,
                            score=log(result["confidence"])
                            + beams[new_beam].last_action.score,
                        )
                        beams[new_beam].last_intent = intent
                        beams[new_beam].rankings.append(intent)
                        graph_gen.create_nodes_highlight_k(
                            {intent.name: round(intent.score.real, 4)},
                            "lightgoldenrod1",
                            beams[new_beam].last_action.name,
                            new_beam,
                            [intent.name],
                        )

            for beam in range(k):
                fallbacks = 0
                for ranking in beams[beam].rankings:
                    if type(ranking) == Intent and ranking.name == "fallback":
                        fallbacks += 1
                if fallbacks >= max_fallbacks:
                    beams[beam].scores = [log(0.00000001)]

    for final in range(len(beams)):
        if beams[final].rollout.get_reached_goal():
            graph_gen.set_last_chosen(beams[final].rankings[-1].name, final)
            graph_gen.complete_conversation(
                round(beams[final].rankings[-1].score.real, 4)
            )
        head = "0"
        for elem in beams[final].rankings:
            tail = head
            # id must be > than the head to prevent referencing previous nodes with the same name
            head = graph_gen.beams[final].parent_nodes_id_map[elem.name].pop(0)
            while int(head) <= int(tail):
                head = graph_gen.beams[final].parent_nodes_id_map[elem.name].pop(0)
            graph_gen.graph.edge(
                tail, head, color="forestgreen", penwidth="10.0", arrowhead="normal"
            )
    graph_gen.graph.render(f"{filename}.gv", view=True)


if __name__ == "__main__":
    icaps_conversation_break_both = [
        {
            "HOVOR": "What invited talk do you want to see on Day 1? You can learn about Factored Transition Systems or the applications of Multi-Agent Path Finding."
        },
        {"USER": "I want to see the talk on Factored Transition Systems."},
        {"HOVOR": "And then? What after the invited talk?"},
        {
            "USER": "I want to learn more about classical planning and why applying heuristics is useful."
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
        {"USER": "I want to see the talk on Factored Transition Systems."},
        {
            "HOVOR": "What session do you want to see in the morning? The sessions available are on Planning Representations and Scheduling, Verification, RL, or Heuristics in Classical Planning."
        },
        {
            "USER": "I want to learn more about classical planning and why applying heuristics is useful."
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
