import json

with open("scratch/leetcode_fallback.json", "r", encoding="utf-8") as f:
    data = json.load(f)

js_code = "const LEETCODE_FALLBACK_QUESTIONS = " + json.dumps(data, indent=2) + ";\n"

with open("scratch/leetcode_fallback.js", "w", encoding="utf-8") as f:
    f.write(js_code)

print("Wrote fallback JS, size:", len(js_code), "bytes")
