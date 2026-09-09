import os

target_dir = "."
keywords = ["leetcode", "csv", "Leetcode"]

for root, dirs, files in os.walk(target_dir):
    if "__pycache__" in root or ".git" in root or "scratch" in root:
        continue
    for file in files:
        if file.endswith((".py", ".js", ".html", ".css", ".md", ".csv")):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                for kw in keywords:
                    if kw in content:
                        print(f"Found '{kw}' in {path}")
                        break
