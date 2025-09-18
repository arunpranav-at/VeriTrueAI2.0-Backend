from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from datetime import datetime, timedelta

from app.schemas.models import AnalyticsData
from app.services.analytics_service import AnalyticsService

router = APIRouter()


async def get_analytics_service() -> AnalyticsService:
    """Dependency to get analytics service."""
    return AnalyticsService()


@router.get("/overview", response_model=AnalyticsData)
async def get_analytics_overview(
    days: int = Query(default=30, ge=1, le=365, description="Number of days for analytics"),
    user_id: Optional[str] = Query(default=None, description="User ID to filter by"),
    analytics_service: AnalyticsService = Depends(get_analytics_service)
) -> AnalyticsData:
    """
    Get comprehensive analytics overview.
    
    Returns analysis statistics, trends, and breakdowns.
    """
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        analytics = await analytics_service.get_overview(start_date, end_date, user_id)
        
        return analytics
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get analytics: {str(e)}")


@router.get("/trends")
async def get_analytics_trends(
    days: int = Query(default=30, ge=1, le=365, description="Number of days for trends"),
    granularity: str = Query(default="daily", regex="^(hourly|daily|weekly)$", description="Trend granularity"),
    analytics_service: AnalyticsService = Depends(get_analytics_service)
):
    """
    Get trend data for analysis patterns.
    
    Returns time-series data showing analysis trends over time.
    """
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        trends = await analytics_service.get_trends(start_date, end_date, granularity)
        
        return trends
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get trends: {str(e)}")


@router.get("/misinformation-patterns")
async def get_misinformation_patterns(
    days: int = Query(default=30, ge=1, le=365, description="Number of days to analyze"),
    analytics_service: AnalyticsService = Depends(get_analytics_service)
):
    """
    Analyze patterns in misinformation detection.
    
    Returns insights about common misinformation types and sources.
    """
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        patterns = await analytics_service.analyze_misinformation_patterns(start_date, end_date)
        
        return patterns
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze patterns: {str(e)}")


@router.get("/source-credibility")
async def get_source_credibility_stats(
    days: int = Query(default=30, ge=1, le=365, description="Number of days to analyze"),
    analytics_service: AnalyticsService = Depends(get_analytics_service)
):
    """
    Get statistics about source credibility.
    
    Returns analysis of source reliability and credibility trends.
    """
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        credibility_stats = await analytics_service.get_source_credibility_stats(start_date, end_date)
        
        return credibility_stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get credibility stats: {str(e)}")


@router.get("/performance")
async def get_performance_metrics(
    days: int = Query(default=7, ge=1, le=30, description="Number of days for performance data"),
    analytics_service: AnalyticsService = Depends(get_analytics_service)
):
    """
    Get system performance metrics.
    
    Returns processing times, error rates, and system health indicators.
    """
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        performance = await analytics_service.get_performance_metrics(start_date, end_date)
        
        return performance
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get performance metrics: {str(e)}")


@router.get("/user-behavior")
async def get_user_behavior_analytics(
    days: int = Query(default=30, ge=1, le=365, description="Number of days to analyze"),
    analytics_service: AnalyticsService = Depends(get_analytics_service)
):
    """
    Analyze user behavior patterns.
    
    Returns insights about how users interact with the system.
    """
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        behavior = await analytics_service.analyze_user_behavior(start_date, end_date)
        
        return behavior
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze user behavior: {str(e)}")


@router.get("/export")
async def export_analytics_data(
    format: str = Query(default="json", regex="^(json|csv)$", description="Export format"),
    days: int = Query(default=30, ge=1, le=365, description="Number of days to export"),
    analytics_service: AnalyticsService = Depends(get_analytics_service)
):
    """
    Export analytics data in specified format.
    
    Supports JSON and CSV formats for further analysis.
    """
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        export_data = await analytics_service.export_data(start_date, end_date, format)
        
        return export_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export data: {str(e)}")