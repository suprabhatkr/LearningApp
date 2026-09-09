from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models.database import User, UserProgress
from app.dependencies import get_current_user
from app.data.sys_design_data import SYSTEM_DESIGN_CHAPTERS, SYSTEM_DESIGN_EXAMPLES

router = APIRouter(prefix="/api/system-design", tags=["System Design"])

@router.get("/chapters")
async def get_chapters():
    return SYSTEM_DESIGN_CHAPTERS

@router.get("/examples")
async def get_examples():
    return SYSTEM_DESIGN_EXAMPLES

@router.post("/chapters/{chapter_id}/complete")
async def complete_chapter(
    chapter_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if chapter_id not in SYSTEM_DESIGN_CHAPTERS:
        raise HTTPException(status_code=404, detail="Chapter not found")
        
    stmt = select(UserProgress).where(
        UserProgress.user_id == current_user.id,
        UserProgress.category == "system_design",
        UserProgress.item_id == chapter_id
    )
    res = await db.execute(stmt)
    progress_entry = res.scalars().first()
    
    if not progress_entry:
        progress_entry = UserProgress(
            user_id=current_user.id,
            category="system_design",
            item_id=chapter_id,
            status="completed"
        )
        db.add(progress_entry)
        current_user.readiness_score = min(100.0, current_user.readiness_score + 3.0)
        await db.commit()
        
    return {"message": "Chapter marked as completed", "readiness_score": current_user.readiness_score}
