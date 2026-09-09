from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from app.database import get_db
from app.models.database import User, UserProgress
from app.dependencies import get_current_user
from app.data.leetcode_questions import LEETCODE_QUESTIONS

router = APIRouter(prefix="/api/leetcode", tags=["Leetcode 100"])

class ToggleRequest(BaseModel):
    solved: bool

@router.get("/questions")
async def get_leetcode_questions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all 100 Leetcode questions.
    Merges default solved states from CSV with the database UserProgress table.
    """
    # 1. Fetch user progress records for this category
    stmt = select(UserProgress).where(
        UserProgress.user_id == current_user.id,
        UserProgress.category == "leetcode"
    )
    res = await db.execute(stmt)
    db_progress = {p.item_id: p.status for p in res.scalars().all()}
    
    # 2. Merge states
    results = []
    for q in LEETCODE_QUESTIONS:
        q_id = q["id"]
        
        # Check if user has overridden the solved state in the DB
        if q_id in db_progress:
            is_solved = db_progress[q_id] == "completed"
        else:
            is_solved = q["default_solved"]
            
        results.append({
            "id": q["id"],
            "name": q["name"],
            "pattern": q["pattern"],
            "difficulty": q["difficulty"],
            "companies": q["companies"],
            "leetcode_url": q["leetcode_url"],
            "solved": is_solved
        })
        
    return results

@router.post("/questions/{question_id}/toggle")
async def toggle_question(
    question_id: str,
    payload: ToggleRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Toggle solved state of a Leetcode question.
    Saves state in DB and modifies user readiness score.
    """
    # Verify if question exists in our dataset
    question = next((q for q in LEETCODE_QUESTIONS if q["id"] == question_id), None)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
        
    # Check current db record
    stmt = select(UserProgress).where(
        UserProgress.user_id == current_user.id,
        UserProgress.category == "leetcode",
        UserProgress.item_id == question_id
    )
    res = await db.execute(stmt)
    progress_entry = res.scalars().first()
    
    status_str = "completed" if payload.solved else "in_progress"
    
    # Calculate score delta (solving a question adds 0.25%, unsolving subtracts 0.25%)
    # Ensure it stays bounded between 0% and 100%
    score_delta = 0.25
    
    # We check if we are actually changing the state
    was_solved = False
    if progress_entry:
        was_solved = progress_entry.status == "completed"
    else:
        was_solved = question["default_solved"]
        
    if payload.solved != was_solved:
        if payload.solved:
            current_user.readiness_score = min(100.0, current_user.readiness_score + score_delta)
        else:
            current_user.readiness_score = max(0.0, current_user.readiness_score - score_delta)
            
    if progress_entry:
        progress_entry.status = status_str
        progress_entry.score = 100.0 if payload.solved else 0.0
    else:
        progress_entry = UserProgress(
            user_id=current_user.id,
            category="leetcode",
            item_id=question_id,
            status=status_str,
            score=100.0 if payload.solved else 0.0
        )
        db.add(progress_entry)
        
    await db.commit()
    
    return {
        "success": True,
        "solved": payload.solved,
        "readiness_score": current_user.readiness_score
    }
