from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Progress metrics
    readiness_score: Mapped[float] = mapped_column(Float, default=68.0)
    streak_days: Mapped[int] = mapped_column(Integer, default=7)
    last_active: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    progress: Mapped[list["UserProgress"]] = relationship("UserProgress", back_populates="user", cascade="all, delete-orphan")
    tracker_items: Mapped[list["UserTrackerItem"]] = relationship("UserTrackerItem", back_populates="user", cascade="all, delete-orphan")


class UserProgress(Base):
    __tablename__ = "user_progress"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Category: "dsa", "system_design", "lld", "ai", "backend"
    category: Mapped[str] = mapped_column(String(30), nullable=False)
    
    # Specific chapter or problem ID
    item_id: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Status: "completed", "in_progress"
    status: Mapped[str] = mapped_column(String(20), default="in_progress")
    
    # Code submission or Quiz answers if applicable
    submission: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Score achieved in quiz (0-100)
    score: Mapped[float] = mapped_column(Float, nullable=True)
    
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="progress")


class UserTrackerItem(Base):
    __tablename__ = "user_tracker_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(50), default="study")
    target: Mapped[str] = mapped_column(String(255), nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    completed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="tracker_items")
