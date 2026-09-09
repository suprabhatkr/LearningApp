from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserResponse(UserBase):
    id: int
    readiness_score: float
    streak_days: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class ProgressUpdate(BaseModel):
    category: str
    item_id: str
    status: str = "completed"
    submission: Optional[str] = None
    score: Optional[float] = None

class ProgressResponse(BaseModel):
    id: int
    category: str
    item_id: str
    status: str
    submission: Optional[str]
    score: Optional[float]
    updated_at: datetime

    class Config:
        from_attributes = True

class CodeSubmitRequest(BaseModel):
    problem_id: str
    code: str

class TestCaseResult(BaseModel):
    input: str
    expected: str
    actual: str
    passed: bool

class CodeSubmitResponse(BaseModel):
    passed: bool
    message: str
    details: List[TestCaseResult]
    runtime_ms: float

class QuizAnswer(BaseModel):
    question_id: str
    selected_option: int

class QuizSubmitRequest(BaseModel):
    quiz_id: str
    answers: List[QuizAnswer]

class QuizQuestionResult(BaseModel):
    question_id: str
    selected_option: int
    correct_option: int
    passed: bool
    explanation: str

class QuizSubmitResponse(BaseModel):
    score: float
    passed: bool
    results: List[QuizQuestionResult]

class DashboardStats(BaseModel):
    readiness_score: float
    streak_days: int
    problems_solved: int
    total_problems: int = 120
    hours_studied: float
    recent_activity: List[ProgressResponse]


class TrackerItemCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    category: str = Field(default="study", min_length=1, max_length=50)
    target: Optional[str] = Field(default=None, max_length=255)
    notes: Optional[str] = None


class TrackerItemUpdate(BaseModel):
    completed: Optional[bool] = None
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    category: Optional[str] = Field(default=None, min_length=1, max_length=50)
    target: Optional[str] = Field(default=None, max_length=255)
    notes: Optional[str] = None


class TrackerItemResponse(BaseModel):
    id: int
    title: str
    category: str
    target: Optional[str]
    notes: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
