import csv
import json

with open("Leetcode 100 questions - Start research.csv", mode="r", encoding="utf-8") as f:
    reader = list(csv.DictReader(f))

questions = []
for r in reader:
    name = r["Problem Name"].strip()
    slug = name.lower().replace(" ", "-").replace("(", "").replace(")", "").replace("'", "").replace(",", "").replace("/", "-")
    url = f"https://leetcode.com/problems/{slug}/"
    questions.append({
        "id": r["#"].strip(),
        "name": name,
        "pattern": r["Core Pattern"].strip(),
        "difficulty": r["Difficulty"].strip(),
        "companies": r["High-Relevance Companies"].strip(),
        "leetcode_url": url,
        "solved": r["Solved"].strip().lower() == "solved"
    })

print("Generated", len(questions), "questions.")

with open("scratch/leetcode_fallback.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2)
