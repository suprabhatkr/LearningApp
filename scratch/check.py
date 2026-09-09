import sys
sys.path.insert(0, '.')
import csv
from app.data.leetcode_questions import LEETCODE_QUESTIONS

with open('Leetcode 100 questions - Start research.csv', mode='r', encoding='utf-8') as f:
    reader = list(csv.DictReader(f))

print('CSV row count:', len(reader))
print('PY questions count:', len(LEETCODE_QUESTIONS))

mismatches = []
for r in reader:
    qid = r['#'].strip()
    py_q = next((q for q in LEETCODE_QUESTIONS if q['id'] == qid), None)
    if not py_q:
        mismatches.append(f"ID {qid} missing in py")
    elif py_q['name'].strip() != r['Problem Name'].strip():
        mismatches.append(f"ID {qid}: CSV '{r['Problem Name']}' vs PY '{py_q['name']}'")

print('Mismatches count:', len(mismatches))
for m in mismatches[:20]:
    print(m)
