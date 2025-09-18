from typing import List
from fastapi import APIRouter, HTTPException, Depends
import time
import uuid

from app.schemas.models import (
    AnalyzeRequest, AnalysisResult, MediaType, VerdicType, ConfidenceLevel
)
from app.services.analysis_service import AnalysisService
from app.services.web_search_service import WebSearchService
from app.services.llm_service import LLMService

router = APIRouter()


async def get_analysis_service() -> AnalysisService:
    """Dependency to get analysis service."""
    return AnalysisService()


async def get_web_search_service() -> WebSearchService:
    """Dependency to get web search service."""
    return WebSearchService()


async def get_llm_service() -> LLMService:
    """Dependency to get LLM service.""" 
    return LLMService()


@router.post("/", response_model=AnalysisResult)
async def analyze_content(
    request: AnalyzeRequest,
    analysis_service: AnalysisService = Depends(get_analysis_service),
    search_service: WebSearchService = Depends(get_web_search_service),
    llm_service: LLMService = Depends(get_llm_service)
) -> AnalysisResult:
    """
    Analyze content for misinformation.
    
    Accepts text, URLs, images, and videos for analysis.
    Returns verdict, confidence, evidence, and reasoning.
    """
    start_time = time.time()
    analysis_id = str(uuid.uuid4())
    
    try:
        # Process the content based on media type
        processed_content = await analysis_service.process_content(
            request.content, request.media_type, request.metadata
        )
        
        # Search for relevant sources
        sources = await search_service.search_sources(processed_content.search_query, limit=10)
        
        # Perform groundedness analysis using LLM
        llm_analysis = await llm_service.analyze_groundedness(
            content=processed_content.text_content,
            sources=sources,
            media_type=request.media_type
        )
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Create analysis result
        result = AnalysisResult(
            id=analysis_id,
            verdict=llm_analysis.verdict,
            confidence=llm_analysis.confidence,
            confidence_score=llm_analysis.confidence_score,
            summary=llm_analysis.summary,
            evidence=sources,
            reasoning=llm_analysis.reasoning,
            processing_time=processing_time
        )
        
        # Store analysis in history (async task)
        await analysis_service.store_analysis(result, request)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/batch", response_model=List[AnalysisResult])
async def analyze_batch(
    requests: List[AnalyzeRequest],
    analysis_service: AnalysisService = Depends(get_analysis_service),
    search_service: WebSearchService = Depends(get_web_search_service),
    llm_service: LLMService = Depends(get_llm_service)
) -> List[AnalysisResult]:
    """
    Analyze multiple content items in batch.
    
    More efficient for processing multiple items at once.
    """
    if len(requests) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 items per batch")
        
    results = []
    for request in requests:
        try:
            # Reuse the single analysis logic
            result = await analyze_content(request, analysis_service, search_service, llm_service)
            results.append(result)
        except Exception as e:
            # For batch processing, we continue with other items if one fails
            error_result = AnalysisResult(
                id=str(uuid.uuid4()),
                verdict=VerdicType.UNVERIFIABLE,
                confidence=ConfidenceLevel.LOW,
                confidence_score=0.0,
                summary=f"Analysis failed: {str(e)}",
                evidence=[],
                reasoning="Unable to process due to error",
                processing_time=0.0
            )
            results.append(error_result)
    
    return results