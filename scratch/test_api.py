import sys
sys.path.insert(0, '.')
from fastapi.testclient import TestClient
from app.main import app

with TestClient(app) as client:
    # 1. Check home page serve
    r_index = client.get("/")
    assert r_index.status_code == 200, "Index page failed"
    print("GET / OK:", len(r_index.text), "bytes")

    # 2. Check CSV serve
    r_csv = client.get("/leetcode-questions.csv")
    assert r_csv.status_code == 200, "CSV serve failed"
    print("GET /leetcode-questions.csv OK:", len(r_csv.text.splitlines()), "lines")

    # 3. Check Register & Auth
    reg_res = client.post("/api/auth/register", json={"username": "senior_candidate", "password": "password123"})
    print("POST /api/auth/register status:", reg_res.status_code)

    token_res = client.post("/api/auth/token", json={"username": "senior_candidate", "password": "password123"})
    assert token_res.status_code == 200, f"Token failed: {token_res.text}"
    token = token_res.json()["access_token"]
    print("POST /api/auth/token OK, token retrieved.")

    headers = {"Authorization": f"Bearer {token}"}

    # 4. Check Me endpoint
    me_res = client.get("/api/auth/me", headers=headers)
    assert me_res.status_code == 200, f"Me failed: {me_res.text}"
    print("GET /api/auth/me OK, user:", me_res.json()["username"])

    # 5. Check LeetCode API Endpoint
    lc_res = client.get("/api/leetcode/questions", headers=headers)
    assert lc_res.status_code == 200, f"Leetcode questions failed: {lc_res.text}"
    questions = lc_res.json()
    assert len(questions) == 100, f"Expected 100 questions, got {len(questions)}"
    print("GET /api/leetcode/questions OK: 100 questions loaded.")
    print("Sample question #1:", questions[0]["name"], "-", questions[0]["pattern"])
    print("Sample question #100:", questions[-1]["name"], "-", questions[-1]["pattern"])

    # 6. Test Toggle Solved
    toggle_res = client.post("/api/leetcode/questions/100/toggle", json={"solved": True}, headers=headers)
    assert toggle_res.status_code == 200, f"Toggle failed: {toggle_res.text}"
    print("POST /api/leetcode/questions/100/toggle OK, result:", toggle_res.json())

print("ALL VERIFICATION TESTS PASSED SUCCESSFULLY!")
