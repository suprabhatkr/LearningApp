import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.dependencies import get_current_user
from app.models.database import User, UserProgress
from app.data.book_data import (
    HLD_BOOK,
    LLD_BOOK,
    HLD_PDF_PATH,
    LLD_PDF_PATH,
    BACKEND_LEARNING_GUIDES,
    chapter_ids,
)

router = APIRouter(prefix="/api/books", tags=["Books"])


def _validate_chapter_id(book, chapter_id: str) -> bool:
    return chapter_id in chapter_ids(book)


def _book_payload(book):
    return {
        "book_id": book["book_id"],
        "title": book["title"],
        "chapters": book["chapters"],
    }


def _backend_guide_payload():
    return {
        "title": "Backend Learning Chapters",
        "chapters": [
            {
                "id": guide["id"],
                "title": guide["title"],
                "summary": guide["summary"],
            }
            for guide in BACKEND_LEARNING_GUIDES
        ],
    }


def _find_backend_guide(guide_id: str):
    for guide in BACKEND_LEARNING_GUIDES:
        if guide["id"] == guide_id:
            return guide
    return None


@router.get("/hld")
async def get_hld_book():
    return _book_payload(HLD_BOOK)


@router.get("/lld")
async def get_lld_book():
    return _book_payload(LLD_BOOK)


@router.get("/backend-learning")
async def get_backend_learning_chapters():
    return _backend_guide_payload()


@router.get("/hld/pdf")
async def get_hld_pdf():
    if not os.path.exists(HLD_PDF_PATH):
        raise HTTPException(status_code=404, detail=f"HLD PDF not found at: {HLD_PDF_PATH}")
    return FileResponse(
        HLD_PDF_PATH,
        media_type="application/pdf",
        headers={"Content-Disposition": 'inline; filename="HLD.pdf"'},
    )


@router.get("/lld/pdf")
async def get_lld_pdf():
    if not os.path.exists(LLD_PDF_PATH):
        raise HTTPException(status_code=404, detail=f"LLD PDF not found at: {LLD_PDF_PATH}")
    return FileResponse(
        LLD_PDF_PATH,
        media_type="application/pdf",
        headers={"Content-Disposition": 'inline; filename="LLD.pdf"'},
    )


@router.get("/backend-learning/{guide_id}/pdf")
async def get_backend_learning_pdf(guide_id: str):
    guide = _find_backend_guide(guide_id)
    if not guide:
        raise HTTPException(status_code=404, detail="Backend learning chapter not found")

    pdf_path = guide["pdf_path"]
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail=f"PDF not found at: {pdf_path}")

    safe_name = f"{guide_id}.pdf"
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        headers={"Content-Disposition": f'inline; filename="{safe_name}"'},
    )


@router.get("/lld/tasks")
async def get_lld_chapter_tasks(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(UserProgress).where(
        UserProgress.user_id == current_user.id,
        UserProgress.category == "lld_book",
    )
    res = await db.execute(stmt)
    progress_rows = res.scalars().all()
    completed_lookup = {
        row.item_id: row.status == "completed"
        for row in progress_rows
        if _validate_chapter_id(LLD_BOOK, row.item_id)
    }

    chapters = []
    completed_count = 0
    for chapter in LLD_BOOK["chapters"]:
        completed = completed_lookup.get(chapter["id"], False)
        if completed:
            completed_count += 1
        chapters.append(
            {
                "chapter_id": chapter["id"],
                "title": chapter["title"],
                "completed": completed,
            }
        )

    return {
        "total": len(LLD_BOOK["chapters"]),
        "completed": completed_count,
        "chapters": chapters,
    }


@router.post("/lld/chapters/{chapter_id}/complete")
async def complete_lld_chapter(
    chapter_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not _validate_chapter_id(LLD_BOOK, chapter_id):
        raise HTTPException(status_code=404, detail="Chapter not found")

    stmt = select(UserProgress).where(
        UserProgress.user_id == current_user.id,
        UserProgress.category == "lld_book",
        UserProgress.item_id == chapter_id,
    )
    res = await db.execute(stmt)
    entry = res.scalars().first()
    newly_completed = False

    if not entry:
        entry = UserProgress(
            user_id=current_user.id,
            category="lld_book",
            item_id=chapter_id,
            status="completed",
        )
        db.add(entry)
        newly_completed = True
    elif entry.status != "completed":
        entry.status = "completed"
        newly_completed = True

    if newly_completed:
        current_user.readiness_score = min(100.0, current_user.readiness_score + 1.0)
        await db.commit()

    return {
        "message": "Chapter task marked as completed",
        "readiness_score": current_user.readiness_score,
    }
