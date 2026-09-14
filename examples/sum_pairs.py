"""Example solver protocol: read one JSON object and emit one JSON value."""
import json, sys

case = json.load(sys.stdin)
nums = case["numbers"]
target = case["target"]
print(json.dumps(sum(1 for i in range(len(nums)) for j in range(i + 1, len(nums)) if nums[i] + nums[j] == target)))
