import hashlib
import uuid
from typing import Optional, Dict, Any
from datetime import datetime

from app.schemas.models import (
    AnalyzeRequest, AnalysisResult, MediaType, VerdicType, ConfidenceLevel
)


class ProcessedContent:
    """Container for processed content data."""
    def __init__(self, text_content: str, search_query: str, metadata: Optional[Dict[str, Any]] = None):
        self.text_content = text_content
        self.search_query = search_query
        self.metadata = metadata or {}


class AnalysisService:
    """Service for handling content analysis operations."""
    
    async def process_content(self, content: str, media_type: MediaType, metadata: Optional[Dict[str, Any]] = None) -> ProcessedContent:
        """
        Process content based on media type and extract searchable text.
        """
        if media_type == MediaType.TEXT:
            return await self._process_text(content, metadata)
        elif media_type == MediaType.URL:
            return await self._process_url(content, metadata)
        elif media_type == MediaType.IMAGE:
            return await self._process_image(content, metadata)
        elif media_type == MediaType.VIDEO:
            return await self._process_video(content, metadata)
        else:
            raise ValueError(f"Unsupported media type: {media_type}")
    
    async def _process_text(self, text: str, metadata: Optional[Dict[str, Any]]) -> ProcessedContent:
        """Process plain text content."""
        # Extract key phrases for search
        search_query = await self._extract_search_query(text)
        
        return ProcessedContent(
            text_content=text,
            search_query=search_query,
            metadata=metadata
        )
    
    async def _process_url(self, url: str, metadata: Optional[Dict[str, Any]]) -> ProcessedContent:
        """Process URL content by extracting text from webpage."""
        try:
            import requests
            from bs4 import BeautifulSoup
            
            # Fetch webpage content
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'VeriTrueAI/2.0 (Misinformation Detection Bot)'
            })
            response.raise_for_status()
            
            # Parse HTML and extract text
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract text from specific elements
            title = soup.find('title')
            title_text = title.get_text().strip() if title else ""
            
            # Get main content
            main_content = ""
            for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'article']):
                main_content += tag.get_text().strip() + " "
            
            # Combine title and content
            text_content = f"{title_text}. {main_content}".strip()
            
            # Generate search query
            search_query = await self._extract_search_query(text_content)
            
            return ProcessedContent(
                text_content=text_content,
                search_query=search_query,
                metadata={**(metadata or {}), "source_url": url, "title": title_text}
            )
            
        except Exception as e:
            # Fallback: use URL as search query
            return ProcessedContent(
                text_content=f"Content from URL: {url}",
                search_query=url,
                metadata={**(metadata or {}), "error": str(e)}
            )
    
    async def _process_image(self, image_path: str, metadata: Optional[Dict[str, Any]]) -> ProcessedContent:
        """Process image content using OCR and image analysis."""
        try:
            # For now, use basic image analysis
            # In a real implementation, you would use:
            # - OCR to extract text from images
            # - Reverse image search
            # - Computer vision for content analysis
            
            search_query = "image analysis verification"
            text_content = f"Image analysis for file: {image_path}"
            
            if metadata and metadata.get("ocr_text"):
                ocr_text = metadata["ocr_text"]
                text_content = f"Text extracted from image: {ocr_text}"
                search_query = await self._extract_search_query(ocr_text)
            
            return ProcessedContent(
                text_content=text_content,
                search_query=search_query,
                metadata={**(metadata or {}), "file_path": image_path}
            )
            
        except Exception as e:
            return ProcessedContent(
                text_content=f"Image analysis error for: {image_path}",
                search_query="image verification",
                metadata={**(metadata or {}), "error": str(e)}
            )
    
    async def _process_video(self, video_path: str, metadata: Optional[Dict[str, Any]]) -> ProcessedContent:
        """Process video content using speech-to-text and video analysis."""
        try:
            # For now, use basic video analysis
            # In a real implementation, you would use:
            # - Speech-to-text for audio track
            # - Frame analysis for visual content
            # - Metadata extraction
            
            search_query = "video content verification"
            text_content = f"Video analysis for file: {video_path}"
            
            if metadata and metadata.get("transcript"):
                transcript = metadata["transcript"]
                text_content = f"Transcript from video: {transcript}"
                search_query = await self._extract_search_query(transcript)
            
            return ProcessedContent(
                text_content=text_content,
                search_query=search_query,
                metadata={**(metadata or {}), "file_path": video_path}
            )
            
        except Exception as e:
            return ProcessedContent(
                text_content=f"Video analysis error for: {video_path}",
                search_query="video verification",
                metadata={**(metadata or {}), "error": str(e)}
            )
    
    async def _extract_search_query(self, text: str) -> str:
        """Extract key phrases from text for search query."""
        # Simple implementation - extract meaningful words
        # In a real implementation, you would use NLP techniques
        import re
        
        # Remove special characters and normalize
        cleaned_text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = cleaned_text.split()
        
        # Filter out common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'will', 'would', 'could', 'should', 'this',
            'that', 'these', 'those', 'it', 'its', 'he', 'she', 'they', 'we', 'you'
        }
        
        meaningful_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Take first 5-10 meaningful words
        query_words = meaningful_words[:8]
        return ' '.join(query_words) if query_words else text[:100]
    
    async def store_analysis(self, result: AnalysisResult, request: AnalyzeRequest) -> None:
        """Store analysis result in history."""
        # In a real implementation, this would store to database
        # For now, we'll just log it
        content_hash = hashlib.md5(request.content.encode()).hexdigest()
        print(f"Storing analysis {result.id} with content hash {content_hash}")
    
    def _calculate_content_hash(self, content: str) -> str:
        """Calculate hash of content for deduplication."""
        return hashlib.md5(content.encode()).hexdigest()