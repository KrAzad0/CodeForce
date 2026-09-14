import json, sys
case = json.load(sys.stdin)
n, target = case["numbers"], case["target"]
print(json.dumps(sum(n[i] + n[j] == target for i in range(len(n)) for j in range(i + 1, len(n)))))
