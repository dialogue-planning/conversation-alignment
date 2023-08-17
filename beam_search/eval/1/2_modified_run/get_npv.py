import json

for kval in [1, 2, 3, 4, 5, 6, 7, 8]:
    with open(f"/home/rebecca/conversation-alignment/beam_search/eval/1/2_modified_run/k_{kval}/output_stats.json", "r") as f:
        results = json.load(f)
        results = results["results"]
        denom = results['tn'] + results['fn']
        if denom == 0:
            print(f"k = {kval}, tn = {results['tn']}, fn = {results['fn']}, npv = N/A")
            continue
        print(f"k = {kval}, tn = {results['tn']}, fn = {results['fn']}, npv = {results['tn']/(denom)}")
        print()