import json

for kval in [1, 2, 3, 4, 5]:
    for fval in [1, 2, 3, 4, 5]:
        with open(f"/home/rebecca/conversation-alignment/beam_search/eval/3/2_modified_run/k_{kval}_f_{fval}/output_stats.json", "r") as f:
            results = json.load(f)
            results = results["results"]
            denom = results['tn'] + results['fn']
            if denom == 0:
                print(f"k = {kval}, f = {fval}, tn = {results['tn']}, fn = {results['fn']}, npv = N/A")
                continue
            print(f"k = {kval}, f = {fval}, tn = {results['tn']}, fn = {results['fn']}, npv = {round(results['tn']/(denom), 2)}")