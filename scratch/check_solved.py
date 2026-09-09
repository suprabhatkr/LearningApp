import sys
sys.path.insert(0, '.')
import csv
from app.data.leetcode_questions import LEETCODE_QUESTIONS

with open('Leetcode 100 questions - Start research.csv', mode='r', encoding='utf-8') as f:
    reader = list(csv.DictReader(f))

solved_mismatches = []
for r in reader:
    qid = r['#'].strip()
    csv_solved = (r['Solved'].strip().lower() == 'solved')
    py_q = next((q for q in LEETCODE_QUESTIONS if q['id'] == qid), None)
    if py_q:
        if py_q['default_solved'] != csv_solved:
            solved_mismatches.append(f"ID {qid} ({r['Problem Name']}): CSV Solved='{r['Solved']}' vs PY default_solved={py_q['default_solved']}")

print("Solved status mismatches:", len(solved_mismatches))
for m in solved_mismatches:
    print(m)
