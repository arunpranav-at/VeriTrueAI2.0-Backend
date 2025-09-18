from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from datetime import datetime, timedelta

from app.schemas.models import AnalysisHistory, MediaType, VerdicType
from app.services.history_service import HistoryService

router = APIRouter()


async def get_history_service() -> HistoryService:
    """Dependency to get history service."""
    return HistoryService()


@router.get("/", response_model=List[AnalysisHistory])
async def get_analysis_history(
    user_id: Optional[str] = Query(default=None, description="User ID to filter by"),
    media_type: Optional[MediaType] = Query(default=None, description="Media type filter"),
    verdict: Optional[VerdicType] = Query(default=None, description="Verdict filter"),
    days: int = Query(default=30, ge=1, le=365, description="Number of days to look back"),
    limit: int = Query(default=50, ge=1, le=500, description="Maximum number of results"),
    offset: int = Query(default=0, ge=0, description="Offset for pagination"),
    history_service: HistoryService = Depends(get_history_service)
) -> List[AnalysisHistory]:
    """
    Get analysis history with optional filters.
    
    Returns historical analysis records based on filters.
    """
    try:
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        history = await history_service.get_history(
            user_id=user_id,
            media_type=media_type,
            verdict=verdict,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            offset=offset
        )
        
        return history
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve history: {str(e)}")


@router.get("/{analysis_id}")
async def get_analysis_detail(
    analysis_id: str,
    history_service: HistoryService = Depends(get_history_service)
):
    """
    Get detailed information about a specific analysis.
    
    Returns full analysis result including evidence and reasoning.
    """
    try:
        analysis = await history_service.get_analysis_by_id(analysis_id)
        
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
            
        return analysis
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve analysis: {str(e)}")


@router.delete("/{analysis_id}")
async def delete_analysis(
    analysis_id: str,
    history_service: HistoryService = Depends(get_history_service)
):
    """
    Delete a specific analysis from history.
    """
    try:
        success = await history_service.delete_analysis(analysis_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Analysis not found")
            
        return {"message": "Analysis deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete analysis: {str(e)}")


@router.delete("/")
async def clear_user_history(
    user_id: str = Query(..., description="User ID"),
    days: Optional[int] = Query(default=None, ge=1, description="Clear history older than N days"),
    history_service: HistoryService = Depends(get_history_service)
):
    """
    Clear analysis history for a user.
    
    Can optionally specify to only clear history older than N days.
    """
    try:
        cutoff_date = None
        if days:
            cutoff_date = datetime.now() - timedelta(days=days)
            
        deleted_count = await history_service.clear_user_history(user_id, cutoff_date)
        
        return {
            "message": f"Cleared {deleted_count} analysis records",
            "user_id": user_id,
            "cutoff_date": cutoff_date
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear history: {str(e)}")


@router.get("/user/{user_id}/summary")
async def get_user_history_summary(
    user_id: str,
    days: int = Query(default=30, ge=1, le=365, description="Number of days to summarize"),
    history_service: HistoryService = Depends(get_history_service)
):
    """
    Get a summary of user's analysis history.
    
    Returns aggregated statistics and trends.
    """
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        summary = await history_service.get_user_summary(user_id, start_date, end_date)
        
        return summary
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user summary: {str(e)}")


@router.get("/search/similar")
async def search_similar_analyses(
    content_hash: str = Query(..., description="Content hash to find similar analyses"),
    threshold: float = Query(default=0.8, ge=0.0, le=1.0, description="Similarity threshold"),
    limit: int = Query(default=10, ge=1, le=50, description="Maximum number of results"),
    history_service: HistoryService = Depends(get_history_service)
) -> List[AnalysisHistory]:
    """
    Find similar analyses based on content similarity.
    
    Useful for detecting repeated misinformation patterns.
    """
    try:
        similar_analyses = await history_service.find_similar_analyses(
            content_hash, threshold, limit
        )
        
        return similar_analyses
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search similar analyses: {str(e)}")