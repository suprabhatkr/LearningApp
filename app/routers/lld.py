from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Dict, Any, List

from app.database import get_db
from app.models.database import User, UserProgress
from app.dependencies import get_current_user
from app.data.lld_data import LLD_CHAPTERS, LLD_QUIZZES
from app.schemas.user_progress import QuizSubmitRequest, QuizSubmitResponse, QuizQuestionResult

router = APIRouter(prefix="/api/lld", tags=["LLD Preparation"])

@router.get("/chapters")
async def get_chapters():
    return LLD_CHAPTERS

@router.get("/quizzes")
async def get_quizzes():
    # Exclude correct options and explanations to avoid cheating
    client_quizzes = {}
    for quiz_id, quiz in LLD_QUIZZES.items():
        client_quizzes[quiz_id] = {
            "title": quiz["title"],
            "questions": [
                {
                    "id": q["id"],
                    "question": q["question"],
                    "options": q["options"]
                }
                for q in quiz["questions"]
            ]
        }
    return client_quizzes

@router.post("/quizzes/{quiz_id}/submit", response_model=QuizSubmitResponse)
async def submit_quiz(
    quiz_id: str,
    payload: QuizSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if quiz_id not in LLD_QUIZZES:
        raise HTTPException(status_code=404, detail="Quiz not found")
        
    quiz = LLD_QUIZZES[quiz_id]
    total_questions = len(quiz["questions"])
    correct_count = 0
    results: List[QuizQuestionResult] = []
    
    # Map questions for fast access
    question_map = {q["id"]: q for q in quiz["questions"]}
    
    for ans in payload.answers:
        if ans.question_id not in question_map:
            continue
        q = question_map[ans.question_id]
        passed = ans.selected_option == q["correct_option"]
        if passed:
            correct_count += 1
            
        results.append(
            QuizQuestionResult(
                question_id=ans.question_id,
                selected_option=ans.selected_option,
                correct_option=q["correct_option"],
                passed=passed,
                explanation=q["explanation"]
            )
        )
        
    score = (correct_count / total_questions) * 100.0 if total_questions > 0 else 0.0
    passed_quiz = score >= 70.0  # 70% to pass
    
    # Save progress
    stmt = select(UserProgress).where(
        UserProgress.user_id == current_user.id,
        UserProgress.category == "lld",
        UserProgress.item_id == quiz_id
    )
    res = await db.execute(stmt)
    progress_entry = res.scalars().first()
    
    status_str = "completed" if passed_quiz else "in_progress"
    
    if not progress_entry:
        progress_entry = UserProgress(
            user_id=current_user.id,
            category="lld",
            item_id=quiz_id,
            status=status_str,
            score=score
        )
        db.add(progress_entry)
    else:
        progress_entry.status = status_str
        progress_entry.score = max(progress_entry.score or 0.0, score)
        
    if passed_quiz:
        current_user.readiness_score = min(100.0, current_user.readiness_score + 4.0)
        
    await db.commit()
    
    return QuizSubmitResponse(
        score=score,
        passed=passed_quiz,
        results=results
    )
