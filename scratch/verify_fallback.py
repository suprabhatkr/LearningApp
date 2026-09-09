import sys
sys.path.insert(0, '.')
import json
from app.data.leetcode_questions import LEETCODE_QUESTIONS

with open("scratch/leetcode_fallback.json", "r", encoding="utf-8") as f:
    generated = json.load(f)

print("Generated count:", len(generated))
print("PY count:", len(LEETCODE_QUESTIONS))

diffs = 0
for g, p in zip(generated, LEETCODE_QUESTIONS):
    if g["id"] != p["id"] or g["name"] != p["name"]:
        print(f"Diff: {g['id']} {g['name']} vs {p['id']} {p['name']}")
        diffs += 1

print("Total diffs:", diffs)
