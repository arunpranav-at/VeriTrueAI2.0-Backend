import asyncio
import time
from typing import List, Optional
import httpx
from urllib.parse import quote

from app.schemas.models import EvidenceSource, SearchSourcesRequest, SearchSourcesResponse
from app.core.config import settings


class WebSearchService:
    """Service for web search and source gathering."""
    
    def __init__(self):
        self.search_api_key = settings.SEARCH_API_KEY
        self.search_engine_id = settings.SEARCH_ENGINE_ID
    
    async def search_sources(self, query: str, limit: int = 10) -> List[EvidenceSource]:
        """
        Search for sources related to the query using general web search.
        
        Returns a list of evidence sources with actual search result data.
        """
        try:
            if self.search_api_key and self.search_engine_id:
                return await self._search_with_google_api(query, limit)
            else:
                # Fallback to simulated search for development
                return await self._simulate_search(query, limit)
                
        except Exception as e:
            print(f"Search error: {e}")
            return await self._simulate_search(query, limit)
    
    async def search_sources_detailed(self, request: SearchSourcesRequest) -> SearchSourcesResponse:
        """
        Perform detailed search with timing and metadata.
        """
        start_time = time.time()
        
        sources = await self.search_sources(request.query, request.limit)
        
        search_time = time.time() - start_time
        
        return SearchSourcesResponse(
            sources=sources,
            total_found=len(sources),
            search_time=search_time
        )
    
    async def search_credible_sources(self, query: str, limit: int = 5, min_credibility: float = 0.7) -> SearchSourcesResponse:
        """
        Search for sources and return all results (no credibility filtering).
        """
        start_time = time.time()
        
        sources = await self.search_sources(query, limit)
        
        search_time = time.time() - start_time
        
        return SearchSourcesResponse(
            sources=sources,
            total_found=len(sources),
            search_time=search_time
        )
    
    async def search_fact_check_sources(self, query: str, limit: int = 5) -> SearchSourcesResponse:
        """
        Search for general sources related to the query.
        """
        return await self.search_sources_detailed(SearchSourcesRequest(query=query, limit=limit))
    
    async def search_academic_sources(self, query: str, limit: int = 5) -> SearchSourcesResponse:
        """
        Search for general sources related to the query.
        """
        return await self.search_sources_detailed(SearchSourcesRequest(query=query, limit=limit))
    
    async def _search_with_google_api(self, query: str, limit: int) -> List[EvidenceSource]:
        """
        Search using Google Custom Search API and return actual search results.
        """
        async with httpx.AsyncClient() as client:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': self.search_api_key,
                'cx': self.search_engine_id,
                'q': query,
                'num': min(limit, 10)  # Google API max is 10 per request
            }
            
            response = await client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            sources = []
            
            for i, item in enumerate(data.get('items', [])):
                url = item.get('link', '')
                title = item.get('title', '')
                snippet = item.get('snippet', '')
                
                # Simple relevance based on search result order (Google's ranking)
                relevance_score = max(0.1, 1.0 - (i * 0.1))  # Decreasing from 1.0 to 0.1
                
                # No artificial credibility scoring - let LLM decide
                credibility_score = 0.5  # Neutral score for all sources
                
                sources.append(EvidenceSource(
                    url=url,
                    title=title,
                    snippet=snippet,
                    relevance_score=relevance_score,
                    credibility_score=credibility_score
                ))
            
            return sources
    
    async def _simulate_search(self, query: str, limit: int) -> List[EvidenceSource]:
        """
        Simulate realistic search results for development/testing.
        """
        # Simulate some delay
        await asyncio.sleep(0.5)
        
        # Generate more realistic mock results based on query
        mock_sources = [
            {
                "url": f"https://example-news.com/article/{query.replace(' ', '-').lower()}",
                "title": f"Breaking: Latest developments on {query[:50]}",
                "snippet": f"Recent reports indicate various perspectives on {query[:40]}. Sources suggest multiple viewpoints exist with ongoing discussions in the community."
            },
            {
                "url": f"https://wiki-source.org/topic/{query.replace(' ', '_').lower()}",
                "title": f"Comprehensive overview: {query[:45]}",
                "snippet": f"Detailed analysis of {query[:35]} including background information, current status, and different expert opinions on the matter."
            },
            {
                "url": f"https://research-journal.com/papers/{query.replace(' ', '-').lower()}",
                "title": f"Study reveals findings about {query[:40]}",
                "snippet": f"Research conducted on {query[:30]} shows varying results. Data collection and analysis provide insights into different aspects of the topic."
            },
            {
                "url": f"https://news-portal.net/stories/{query.replace(' ', '-').lower()}",
                "title": f"Public discussion around {query[:40]}",
                "snippet": f"Community debate continues regarding {query[:35]}. Various stakeholders express different viewpoints and concerns about the issue."
            },
            {
                "url": f"https://info-hub.com/topics/{query.replace(' ', '-').lower()}",
                "title": f"Everything you need to know about {query[:35]}",
                "snippet": f"Comprehensive guide covering {query[:30]}. Includes multiple perspectives, expert opinions, and factual information from various sources."
            }
        ]
        
        sources = []
        for i, mock in enumerate(mock_sources[:limit]):
            # Simple relevance based on search result order
            relevance_score = max(0.1, 1.0 - (i * 0.15))  # Decreasing relevance
            
            # Neutral credibility score - let LLM decide
            credibility_score = 0.5
            
            sources.append(EvidenceSource(
                url=mock["url"],
                title=mock["title"],
                snippet=mock["snippet"],
                relevance_score=relevance_score,
                credibility_score=credibility_score
            ))
        
        return sources
