import sys
import os
import time
import tempfile
import subprocess
from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models.database import User, UserProgress
from app.schemas.user_progress import CodeSubmitRequest, CodeSubmitResponse, TestCaseResult
from app.dependencies import get_current_user
from app.data.dsa_data import DSA_TOPICS, DSA_PROBLEMS

router = APIRouter(prefix="/api/dsa", tags=["DSA Preparation"])

@router.get("/topics")
async def get_topics():
    return DSA_TOPICS

@router.get("/problems")
async def get_problems():
    # Return basic fields, avoid exposing eval script to client
    return [
        {
            "id": p["id"],
            "title": p["title"],
            "difficulty": p["difficulty"],
            "description": p["description"],
            "starter_code": p["starter_code"],
            "test_cases": p["test_cases"]
        }
        for p in DSA_PROBLEMS
    ]

@router.get("/problems/{problem_id}")
async def get_problem(problem_id: str):
    for p in DSA_PROBLEMS:
        if p["id"] == problem_id:
            return {
                "id": p["id"],
                "title": p["title"],
                "difficulty": p["difficulty"],
                "description": p["description"],
                "starter_code": p["starter_code"],
                "test_cases": p["test_cases"]
            }
    raise HTTPException(status_code=404, detail="Problem not found")

@router.post("/problems/{problem_id}/submit", response_model=CodeSubmitResponse)
async def submit_problem(
    problem_id: str,
    payload: CodeSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Find problem
    problem = None
    for p in DSA_PROBLEMS:
        if p["id"] == problem_id:
            problem = p
            break
            
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    # Safe Local Code Execution
    # Prepare script content
    full_script = f"""
# USER CODE SUBMISSION:
{payload.code}

# EVALUATION RUNNER:
{problem["eval_script"]}
"""

    temp_file_path = None
    try:
        # Create a temp file
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w", encoding="utf-8") as temp_file:
            temp_file.write(full_script)
            temp_file_path = temp_file.name

        # Run process
        start_time = time.perf_counter()
        
        # We run the script in a separate python process for safety and isolation
        # Timeout of 3 seconds prevents infinite loops
        result = subprocess.run(
            ["py", temp_file_path],
            capture_output=True,
            text=True,
            timeout=3.0
        )
        
        end_time = time.perf_counter()
        runtime_ms = (end_time - start_time) * 1000.0
        
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        
        passed = False
        message = ""
        
        if result.returncode == 0:
            if "PASSED" in stdout:
                passed = True
                message = "All test cases passed successfully!"
            else:
                passed = False
                message = "Incorrect submission. Some test cases failed."
        else:
            passed = False
            message = "Runtime Error / Syntax Error."
            stdout = stderr if stderr else stdout

    except subprocess.TimeoutExpired:
        passed = False
        message = "Execution Timed Out (Infinite loop or slow algorithm)."
        stdout = "Time limit exceeded (3.0 seconds)."
        runtime_ms = 3000.0
    except Exception as e:
        passed = False
        message = f"Executor error occurred."
        stdout = str(e)
        runtime_ms = 0.0
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    # Save progress to database
    # Check if entry already exists
    stmt = select(UserProgress).where(
        UserProgress.user_id == current_user.id,
        UserProgress.category == "dsa",
        UserProgress.item_id == problem_id
    )
    res = await db.execute(stmt)
    progress_entry = res.scalars().first()
    
    status_str = "completed" if passed else "in_progress"
    
    if progress_entry:
        progress_entry.status = status_str
        progress_entry.submission = payload.code
        progress_entry.score = 100.0 if passed else 0.0
    else:
        progress_entry = UserProgress(
            user_id=current_user.id,
            category="dsa",
            item_id=problem_id,
            status=status_str,
            submission=payload.code,
            score=100.0 if passed else 0.0
        )
        db.add(progress_entry)

    # Increment user readiness score slightly on pass
    if passed and status_str == "completed":
        # Increment readiness score by 2% max 100%
        current_user.readiness_score = min(100.0, current_user.readiness_score + 2.5)
        
    await db.commit()

    # Formulate test case details structure
    details = [
        TestCaseResult(
            input=str(problem["test_cases"][0]["input"]),
            expected=str(problem["test_cases"][0]["expected"]),
            actual=stdout if not passed else str(problem["test_cases"][0]["expected"]),
            passed=passed
        )
    ]

    return CodeSubmitResponse(
        passed=passed,
        message=message,
        details=details,
        runtime_ms=round(runtime_ms, 2)
    )
