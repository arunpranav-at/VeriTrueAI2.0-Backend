from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl
from enum import Enum
from datetime import datetime


class MediaType(str, Enum):
    """Supported media types for analysis."""
    TEXT = "text"
    URL = "url"
    IMAGE = "image"
    VIDEO = "video"


class VerdicType(str, Enum):
    """Analysis verdict types."""
    TRUE = "true"
    FALSE = "false"
    PARTIALLY_TRUE = "partially_true"
    MISLEADING = "misleading"
    UNVERIFIABLE = "unverifiable"


class ConfidenceLevel(str, Enum):
    """Confidence levels for analysis."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class AnalyzeRequest(BaseModel):
    """Request model for content analysis."""
    content: str = Field(..., description="Content to analyze (text, URL, or file path)")
    media_type: MediaType = Field(..., description="Type of media being analyzed")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class EvidenceSource(BaseModel):
    """Source evidence model."""
    url: HttpUrl
    title: str
    snippet: str
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    credibility_score: float = Field(..., ge=0.0, le=1.0)


class AnalysisResult(BaseModel):
    """Analysis result model."""
    id: str = Field(..., description="Unique analysis ID")
    verdict: VerdicType = Field(..., description="Analysis verdict")
    confidence: ConfidenceLevel = Field(..., description="Confidence level")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Numerical confidence score")
    summary: str = Field(..., description="Summary of the analysis")
    evidence: List[EvidenceSource] = Field(default=[], description="Supporting evidence")
    reasoning: str = Field(..., description="AI reasoning for the verdict")
    timestamp: datetime = Field(default_factory=datetime.now)
    processing_time: float = Field(..., description="Processing time in seconds")


class SearchSourcesRequest(BaseModel):
    """Request model for source searching."""
    query: str = Field(..., description="Search query")
    limit: int = Field(default=10, ge=1, le=50, description="Maximum number of sources")


class SearchSourcesResponse(BaseModel):
    """Response model for source searching."""
    sources: List[EvidenceSource]
    total_found: int
    search_time: float


class AnalysisHistory(BaseModel):
    """Historical analysis record."""
    id: str
    content_hash: str
    media_type: MediaType
    verdict: VerdicType
    confidence: ConfidenceLevel
    timestamp: datetime
    user_id: Optional[str] = None


class AnalyticsData(BaseModel):
    """Analytics data model."""
    total_analyses: int
    verdicts_breakdown: Dict[str, int]
    confidence_breakdown: Dict[str, int]
    media_type_breakdown: Dict[str, int]
    average_processing_time: float
    date_range: Dict[str, datetime]


class UserSettings(BaseModel):
    """User settings model."""
    user_id: str
    preferences: Dict[str, Any] = Field(default={})
    notification_settings: Dict[str, bool] = Field(default={})
    analysis_history_retention: int = Field(default=90, description="Days to retain history")


class HealthStatus(BaseModel):
    """Health check status."""
    status: str
    timestamp: datetime = Field(default_factory=datetime.now)
    services: Dict[str, str] = Field(default={})
    version: str = "2.0.0"