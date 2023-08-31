import json

with open("/home/rebecca/conversation-alignment/beam_search/eval/1/2_modified_run/results.csv", "w") as csv:
    csv.write("Iterations,TA,FA,TM,FM,Drop-off Nodes")
    for i in range(1, exclusive_stop):
        with open(f"/home/rebecca/conversation-alignment/beam_search/eval/1/2_modified_run/iter_{i}/output_stats.json", "r") as f:
            results = json.load(f)
            results = results["results"]
        csv.write(f"{i},{results['tp']},{results['fp']},{results['tn']},{results['fn']},{sum(results['drop-off nodes'].values())}")