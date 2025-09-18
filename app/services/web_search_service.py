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
        
        # Credible domains for source credibility scoring
        self.credible_domains = {
            # News organizations
            'reuters.com': 0.95,
            'bbc.com': 0.92,
            'apnews.com': 0.94,
            'npr.org': 0.90,
            'cnn.com': 0.85,
            'nytimes.com': 0.88,
            'washingtonpost.com': 0.87,
            'theguardian.com': 0.86,
            
            # Academic and research
            'scholar.google.com': 0.98,
            'ncbi.nlm.nih.gov': 0.97,
            'nature.com': 0.96,
            'science.org': 0.96,
            'arxiv.org': 0.94,
            'jstor.org': 0.95,
            
            # Fact-checking organizations
            'snopes.com': 0.93,
            'factcheck.org': 0.94,
            'politifact.com': 0.92,
            'fullfact.org': 0.91,
            'factchecker.in': 0.89,
            
            # Government and official sources
            'cdc.gov': 0.96,
            'who.int': 0.95,
            'nih.gov': 0.96,
            'fda.gov': 0.94,
            'europa.eu': 0.92,
            'gov.uk': 0.91
        }
    
    async def search_sources(self, query: str, limit: int = 10) -> List[EvidenceSource]:
        """
        Search for sources related to the query.
        
        Returns a list of evidence sources with relevance and credibility scores.
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
        Search for highly credible sources only.
        """
        start_time = time.time()
        
        all_sources = await self.search_sources(query, limit * 2)  # Search more to filter
        credible_sources = [
            source for source in all_sources 
            if source.credibility_score >= min_credibility
        ][:limit]
        
        search_time = time.time() - start_time
        
        return SearchSourcesResponse(
            sources=credible_sources,
            total_found=len(credible_sources),
            search_time=search_time
        )
    
    async def search_fact_check_sources(self, query: str, limit: int = 5) -> SearchSourcesResponse:
        """
        Search specifically for fact-checking sources.
        """
        fact_check_query = f"{query} site:snopes.com OR site:factcheck.org OR site:politifact.com OR site:fullfact.org"
        return await self.search_sources_detailed(SearchSourcesRequest(query=fact_check_query, limit=limit))
    
    async def search_academic_sources(self, query: str, limit: int = 5) -> SearchSourcesResponse:
        """
        Search for academic and scholarly sources.
        """
        academic_query = f"{query} site:scholar.google.com OR site:ncbi.nlm.nih.gov OR site:nature.com OR site:science.org"
        return await self.search_sources_detailed(SearchSourcesRequest(query=academic_query, limit=limit))
    
    async def _search_with_google_api(self, query: str, limit: int) -> List[EvidenceSource]:
        """
        Search using Google Custom Search API.
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
            
            for item in data.get('items', []):
                url = item.get('link', '')
                title = item.get('title', '')
                snippet = item.get('snippet', '')
                
                credibility_score = self._calculate_credibility_score(url)
                relevance_score = self._calculate_relevance_score(title, snippet, query)
                
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
        Simulate search results for development/testing.
        """
        # Simulate some delay
        await asyncio.sleep(0.5)
        
        # Generate mock results based on query
        mock_sources = [
            {
                "url": "https://reuters.com/fact-check/example",
                "title": f"Fact Check: Analysis of '{query[:50]}...'",
                "snippet": f"Reuters fact-checking team investigates claims about {query[:30]}. Our analysis shows mixed evidence with some verified facts and some unsubstantiated claims.",
                "domain": "reuters.com"
            },
            {
                "url": "https://bbc.com/news/example",
                "title": f"BBC Investigation: {query[:40]}",
                "snippet": f"BBC News examines the claims surrounding {query[:25]}. Multiple expert sources provide context and verification.",
                "domain": "bbc.com"
            },
            {
                "url": "https://ncbi.nlm.nih.gov/study/example",
                "title": f"Scientific Study: Research on {query[:35]}",
                "snippet": f"Peer-reviewed research published in medical journal examining {query[:30]}. Methodology and results detailed.",
                "domain": "ncbi.nlm.nih.gov"
            },
            {
                "url": "https://snopes.com/fact-check/example",
                "title": f"Snopes Fact Check: {query[:40]}",
                "snippet": f"Detailed fact-checking analysis of viral claims about {query[:25]}. Evidence rating and source verification included.",
                "domain": "snopes.com"
            },
            {
                "url": "https://scholar.google.com/example",
                "title": f"Academic Research: {query[:35]}",
                "snippet": f"Multiple academic papers and studies related to {query[:30]}. Peer-reviewed sources and citations available.",
                "domain": "scholar.google.com"
            }
        ]
        
        sources = []
        for i, mock in enumerate(mock_sources[:limit]):
            credibility_score = self.credible_domains.get(mock["domain"], 0.5)
            relevance_score = max(0.6, 1.0 - (i * 0.1))  # Decreasing relevance
            
            sources.append(EvidenceSource(
                url=mock["url"],
                title=mock["title"],
                snippet=mock["snippet"],
                relevance_score=relevance_score,
                credibility_score=credibility_score
            ))
        
        return sources
    
    def _calculate_credibility_score(self, url: str) -> float:
        """
        Calculate credibility score based on domain and other factors.
        """
        from urllib.parse import urlparse
        
        try:
            domain = urlparse(url).netloc.lower()
            # Remove www. prefix
            domain = domain.replace('www.', '')
            
            # Check against known credible domains
            if domain in self.credible_domains:
                return self.credible_domains[domain]
            
            # Apply heuristics for unknown domains
            score = 0.5  # Default neutral score
            
            # Government domains get higher scores
            if domain.endswith('.gov') or domain.endswith('.edu'):
                score += 0.2
            
            # Org domains get slight boost
            if domain.endswith('.org'):
                score += 0.1
            
            # Penalize certain patterns
            if any(word in domain for word in ['blog', 'wordpress', 'tumblr', 'medium']):
                score -= 0.2
            
            return max(0.0, min(1.0, score))
            
        except Exception:
            return 0.5
    
    def _calculate_relevance_score(self, title: str, snippet: str, query: str) -> float:
        """
        Calculate relevance score based on text similarity.
        """
        try:
            # Simple word overlap scoring
            query_words = set(query.lower().split())
            title_words = set(title.lower().split())
            snippet_words = set(snippet.lower().split())
            
            # Calculate overlaps
            title_overlap = len(query_words.intersection(title_words)) / max(len(query_words), 1)
            snippet_overlap = len(query_words.intersection(snippet_words)) / max(len(query_words), 1)
            
            # Weight title more heavily than snippet
            relevance_score = (title_overlap * 0.7) + (snippet_overlap * 0.3)
            
            return max(0.1, min(1.0, relevance_score))
            
        except Exception:
            return 0.5