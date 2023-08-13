import json
import random
from typing import Dict


def write_to_file(actions: Dict, partial: Dict, rollout_config: Dict, path: str):
    rollout_config["actions"] = actions
    rollout_config["partial"] = {act: list(out) for act, out in partial.items()}
    with open(path, "w") as f:
        f.write(json.dumps(rollout_config, indent=4))


def read_from_file(path: str):
    with open(path, "r") as f:
        rollout_config = json.load(f)
    return rollout_config, rollout_config["actions"], {act: set() for act in rollout_config["actions"]}


def del_fluent_from_rollout(fluent_name: str, path: str):
    rollout_config, actions, partial = read_from_file(path)
    for act, act_cfg in actions.items():
        if fluent_name in act_cfg["condition"]:
            # note that we don't include conditions in `partial` because deleting
            # a condition makes the action applicable in MORE states
            act_cfg["condition"].remove(fluent_name)
        for out in act_cfg["effect"]:
            if fluent_name in act_cfg["effect"][out]:
                act_cfg["effect"][out].remove(fluent_name)
                partial[act].add(out)
    write_to_file(actions, partial, rollout_config, path)


def del_from_rollout(num_delete: int, path: str):
    rollout_config, actions, partial = read_from_file(path)
    idx = 0
    skip_acts = set()
    random.seed(925)
    while idx < num_delete:
        # first randomly select an action that we haven't yet determined is empty
        available_acts = [act for act in actions if act not in skip_acts]
        if not available_acts:
            break
        act = random.choice(available_acts)
        # filter by outcomes that have at least one fluent
        filtered_outs = [
            out for out, out_cfg in actions[act]["effect"].items() if len(out_cfg) > 0
        ]
        if not filtered_outs:
            skip_acts.add(act)
            continue
        outcome = random.choice(filtered_outs)
        partial[act].add(outcome)
        fl = random.choice(actions[act]["effect"][outcome])
        actions[act]["effect"][outcome].remove(fl)
        idx += 1
    write_to_file(actions, partial, rollout_config, path)


def del_percent_from_rollout(percent: float, path: str):
    _, actions, _ = read_from_file(path)
    num_fluents = 0
    for _, act_cfg in actions.items():
        for _, out in act_cfg["effect"].items():
            num_fluents += len(out)
    del_from_rollout(int(percent * num_fluents), path)


def add_fluent(correct_rollout_path, rollout_path, action, outcome, fluent):
    rollout_config, actions, _ = read_from_file(rollout_path)
    with open(correct_rollout_path, "r") as f:
        correct_rollout = json.load(f)

    rollout_config["actions"][action]["effect"][outcome].append(fluent)

    for act, act_cfg in actions.items():
        for out, fluents in act_cfg["effect"].items():
            if set(fluents) == set(correct_rollout["actions"][act]["effect"][out]) and out in rollout_config["partial"][act]:
                rollout_config["partial"][act].remove(out)
    write_to_file(actions, rollout_config["partial"], rollout_config, rollout_path)


if __name__ == "__main__":
    del_from_rollout(
        1,
        "beam_search\\eval\\1\\2_modified_run\\output_files\\rollout_config.json"
    )
    # add_fluent(
    #     "beam_search/eval/2/1_unmodified_run/output_files/rollout_config.json", 
    #     "beam_search/eval/2/2_modified_run/output_files/rollout_config.json",
    #     "set-restaurant",
    #     "set-restaurant_DETDUP_set-restaurant__assign_restaurant-EQ-set-chinese",
    #     "(know__restaurant)"
    # )
