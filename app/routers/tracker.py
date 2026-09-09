from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import case
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.dependencies import get_current_user
from app.models.database import User, UserTrackerItem
from app.schemas.user_progress import TrackerItemCreate, TrackerItemResponse, TrackerItemUpdate

router = APIRouter(prefix="/api/tracker", tags=["Progress Tracker"])


@router.get("/items", response_model=list[TrackerItemResponse])
async def get_tracker_items(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(UserTrackerItem)
        .where(UserTrackerItem.user_id == current_user.id)
        .order_by(case((UserTrackerItem.completed.is_(False), 0), else_=1), UserTrackerItem.updated_at.desc())
    )
    res = await db.execute(stmt)
    return res.scalars().all()


@router.post("/items", response_model=TrackerItemResponse)
async def create_tracker_item(
    payload: TrackerItemCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    entry = UserTrackerItem(
        user_id=current_user.id,
        title=payload.title.strip(),
        category=payload.category.strip(),
        target=payload.target.strip() if payload.target else None,
        notes=payload.notes.strip() if payload.notes else None,
        completed=False,
    )
    db.add(entry)
    await db.flush()
    return entry


@router.patch("/items/{item_id}", response_model=TrackerItemResponse)
async def update_tracker_item(
    item_id: int,
    payload: TrackerItemUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(UserTrackerItem).where(
        UserTrackerItem.id == item_id,
        UserTrackerItem.user_id == current_user.id,
    )
    res = await db.execute(stmt)
    entry = res.scalars().first()
    if not entry:
        raise HTTPException(status_code=404, detail="Tracker item not found")

    if payload.completed is not None:
        entry.completed = payload.completed
    if payload.title is not None:
        entry.title = payload.title.strip()
    if payload.category is not None:
        entry.category = payload.category.strip()
    if payload.target is not None:
        entry.target = payload.target.strip() if payload.target else None
    if payload.notes is not None:
        entry.notes = payload.notes.strip() if payload.notes else None

    return entry


@router.delete("/items/{item_id}")
async def delete_tracker_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(UserTrackerItem).where(
        UserTrackerItem.id == item_id,
        UserTrackerItem.user_id == current_user.id,
    )
    res = await db.execute(stmt)
    entry = res.scalars().first()
    if not entry:
        raise HTTPException(status_code=404, detail="Tracker item not found")

    await db.delete(entry)
    return {"message": "Tracker item deleted"}
