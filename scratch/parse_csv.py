import csv
import re

csv_path = r"C:\Users\supra\Downloads\Leetcode 100 questions - Start research.csv"
output_path = r"C:\Users\supra\Developer\Coding\learningWebsite\app\data\leetcode_questions.py"

overrides = {
    "Add and Search Word - Data structure design": "design-add-and-search-words-data-structure",
    "Encode and Decode Strings": "encode-and-decode-strings",
    "Implement Trie (Prefix Tree)": "implement-trie-prefix-tree",
}

questions = []

with open(csv_path, mode='r', encoding='utf-8') as f:
    # Some CSVs have a BOM
    first_char = f.read(1)
    if first_char != '\ufeff':
        f.seek(0)
    
    reader = csv.DictReader(f)
    for row in reader:
        # Check column names
        num = row.get('#')
        name = row.get('Problem Name')
        pattern = row.get('Core Pattern')
        difficulty = row.get('Difficulty')
        companies = row.get('High-Relevance Companies')
        solved_str = row.get('Solved')
        
        # Strip whitespace
        name = name.strip() if name else ""
        pattern = pattern.strip() if pattern else ""
        difficulty = difficulty.strip() if difficulty else ""
        companies = companies.strip() if companies else ""
        solved_str = solved_str.strip() if solved_str else ""
        
        if not name:
            continue
            
        # Slugification
        if name in overrides:
            slug = overrides[name]
        else:
            slug = re.sub(r'[^a-zA-Z0-9\s-]', '', name).strip().lower()
            slug = re.sub(r'[\s-]+', '-', slug)
            
        leetcode_url = f"https://leetcode.com/problems/{slug}/"
        solved = solved_str.lower() == "solved"
        
        questions.append({
            "id": num,
            "name": name,
            "pattern": pattern,
            "difficulty": difficulty,
            "companies": companies,
            "leetcode_url": leetcode_url,
            "solved": solved
        })

# Now write app/data/leetcode_questions.py
with open(output_path, mode='w', encoding='utf-8') as f:
    f.write("# Generated from LeetCode CSV file\n\n")
    f.write("LEETCODE_QUESTIONS = [\n")
    for q in questions:
        f.write(f"    {{\n")
        f.write(f"        \"id\": \"{q['id']}\",\n")
        f.write(f"        \"name\": \"{q['name']}\",\n")
        f.write(f"        \"pattern\": \"{q['pattern']}\",\n")
        f.write(f"        \"difficulty\": \"{q['difficulty']}\",\n")
        f.write(f"        \"companies\": \"{q['companies']}\",\n")
        f.write(f"        \"leetcode_url\": \"{q['leetcode_url']}\",\n")
        f.write(f"        \"default_solved\": {q['solved']}\n")
        f.write(f"    }},\n")
    f.write("]\n")

print(f"Parsed {len(questions)} questions successfully.")
