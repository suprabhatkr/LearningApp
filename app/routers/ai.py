from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Dict, Any, List

from app.database import get_db
from app.models.database import User, UserProgress
from app.dependencies import get_current_user
from app.data.ai_data import AI_CHAPTERS, AI_QUIZ, AI_REFERENCE_PDFS
from app.schemas.user_progress import QuizSubmitRequest, QuizSubmitResponse, QuizQuestionResult

router = APIRouter(prefix="/api/ai", tags=["AI Learning"])

@router.get("/chapters")
async def get_chapters():
    return AI_CHAPTERS


@router.get("/references")
async def get_references():
    return {
        "items": [
            {
                "id": ref["id"],
                "week": ref["week"],
                "title": ref["title"],
                "filename": ref["filename"],
                "pdf_url": f"/api/ai/references/{ref['id']}/pdf",
                "available": Path(ref["path"]).exists(),
            }
            for ref in AI_REFERENCE_PDFS
        ]
    }


@router.get("/references/{reference_id}/pdf")
async def get_reference_pdf(reference_id: str):
    ref = next((item for item in AI_REFERENCE_PDFS if item["id"] == reference_id), None)
    if not ref:
        raise HTTPException(status_code=404, detail="Reference not found")
    pdf_path = Path(ref["path"])
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail=f"PDF not found: {ref['filename']}")

    return FileResponse(
        str(pdf_path),
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename=\"{ref['filename']}\""},
    )

@router.get("/quizzes")
async def get_quizzes():
    # Returns the quiz structure without answers
    return {
        "ai_general_quiz": {
            "title": AI_QUIZ["title"],
            "questions": [
                {
                    "id": q["id"],
                    "question": q["question"],
                    "options": q["options"]
                }
                for q in AI_QUIZ["questions"]
            ]
        }
    }

@router.post("/quizzes/{quiz_id}/submit", response_model=QuizSubmitResponse)
async def submit_ai_quiz(
    quiz_id: str,
    payload: QuizSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if quiz_id != "ai_general_quiz":
        raise HTTPException(status_code=404, detail="AI Quiz not found")
        
    total_questions = len(AI_QUIZ["questions"])
    correct_count = 0
    results: List[QuizQuestionResult] = []
    
    # Map questions for fast access
    question_map = {q["id"]: q for q in AI_QUIZ["questions"]}
    
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
    passed_quiz = score >= 66.0  # 66% to pass
    
    # Save progress
    stmt = select(UserProgress).where(
        UserProgress.user_id == current_user.id,
        UserProgress.category == "ai",
        UserProgress.item_id == quiz_id
    )
    res = await db.execute(stmt)
    progress_entry = res.scalars().first()
    
    status_str = "completed" if passed_quiz else "in_progress"
    
    if not progress_entry:
        progress_entry = UserProgress(
            user_id=current_user.id,
            category="ai",
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
