import json

with open(f"/home/rebecca/conversation-alignment/beam_search/eval/2/2_modified_run/data.csv", "w") as csv:
    for i in range(1, 19):
        with open(f"/home/rebecca/conversation-alignment/beam_search/eval/2/2_modified_run/{i}_iter/output_stats.json", "r") as f:
            results = json.load(f)
            results = results["results"]
            print(f"tp = {results['tp']}, fp = {results['fp']}, tn = {results['tn']}, fn = {results['fn']}, drop-off nodes = {sum(results['drop-off nodes'].values())}")
            csv.write(f"{results['tp']},{results['fp']},{results['tn']},{results['fn']},{sum(results['drop-off nodes'].values())}\n")