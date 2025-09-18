from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional

from app.schemas.models import SearchSourcesRequest, SearchSourcesResponse
from app.services.web_search_service import WebSearchService

router = APIRouter()


async def get_web_search_service() -> WebSearchService:
    """Dependency to get web search service."""
    return WebSearchService()


@router.get("/", response_model=SearchSourcesResponse)
async def search_sources(
    query: str = Query(..., description="Search query"),
    limit: int = Query(default=10, ge=1, le=50, description="Maximum number of sources"),
    search_service: WebSearchService = Depends(get_web_search_service)
) -> SearchSourcesResponse:
    """
    Search for relevant sources based on a query.
    
    Returns credible sources that can be used as evidence.
    """
    try:
        # Create request object
        request = SearchSourcesRequest(query=query, limit=limit)
        
        # Perform search
        response = await search_service.search_sources_detailed(request)
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.post("/", response_model=SearchSourcesResponse)
async def search_sources_post(
    request: SearchSourcesRequest,
    search_service: WebSearchService = Depends(get_web_search_service)
) -> SearchSourcesResponse:
    """
    Search for relevant sources (POST version for complex queries).
    
    Allows for more complex search parameters and filters.
    """
    try:
        response = await search_service.search_sources_detailed(request)
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/credible")
async def search_credible_sources(
    query: str = Query(..., description="Search query"),
    limit: int = Query(default=5, ge=1, le=20, description="Maximum number of sources"),
    min_credibility: float = Query(default=0.7, ge=0.0, le=1.0, description="Minimum credibility score"),
    search_service: WebSearchService = Depends(get_web_search_service)
) -> SearchSourcesResponse:
    """
    Search for highly credible sources only.
    
    Filters results to only include sources above the minimum credibility threshold.
    """
    try:
        # Perform search with credibility filter
        response = await search_service.search_credible_sources(
            query=query,
            limit=limit,
            min_credibility=min_credibility
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Credible source search failed: {str(e)}")


@router.get("/fact-check")
async def search_fact_check_sources(
    query: str = Query(..., description="Search query"),
    limit: int = Query(default=5, ge=1, le=20, description="Maximum number of sources"),
    search_service: WebSearchService = Depends(get_web_search_service)
) -> SearchSourcesResponse:
    """
    Search specifically for fact-checking sources.
    
    Focuses on established fact-checking organizations and their content.
    """
    try:
        response = await search_service.search_fact_check_sources(query, limit)
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fact-check search failed: {str(e)}")


@router.get("/academic")
async def search_academic_sources(
    query: str = Query(..., description="Search query"),
    limit: int = Query(default=5, ge=1, le=20, description="Maximum number of sources"),
    search_service: WebSearchService = Depends(get_web_search_service)
) -> SearchSourcesResponse:
    """
    Search for academic and scholarly sources.
    
    Focuses on peer-reviewed publications and academic institutions.
    """
    try:
        response = await search_service.search_academic_sources(query, limit)
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Academic search failed: {str(e)}")