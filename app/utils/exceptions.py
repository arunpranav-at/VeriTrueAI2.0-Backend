from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import traceback
from typing import Union

from app.utils.logging import get_logger

logger = get_logger(__name__)


class VeriTrueAIException(Exception):
    """Base exception for VeriTrueAI application."""
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class AnalysisException(VeriTrueAIException):
    """Exception raised during content analysis."""
    pass


class SearchException(VeriTrueAIException):
    """Exception raised during source searching."""
    pass


class FileProcessingException(VeriTrueAIException):
    """Exception raised during file processing."""
    pass


class LLMException(VeriTrueAIException):
    """Exception raised during LLM operations."""
    pass


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    logger.error(
        "HTTP exception occurred",
        status_code=exc.status_code,
        detail=exc.detail,
        path=request.url.path,
        method=request.method
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.detail,
                "type": "http_error",
                "status_code": exc.status_code
            }
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation exceptions."""
    logger.error(
        "Validation error",
        errors=exc.errors(),
        path=request.url.path,
        method=request.method
    )
    
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "message": "Validation error",
                "type": "validation_error",
                "details": exc.errors()
            }
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(
        "Unhandled exception",
        exception=str(exc),
        traceback=traceback.format_exc(),
        path=request.url.path,
        method=request.method
    )
    
    # Don't expose internal errors in production
    error_message = "Internal server error"
    if hasattr(exc, 'message'):
        error_message = exc.message
    
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "message": error_message,
                "type": "internal_error",
                "error_code": getattr(exc, 'error_code', None)
            }
        }
    )


async def veritrue_exception_handler(request: Request, exc: VeriTrueAIException):
    """Handle custom VeriTrueAI exceptions."""
    logger.error(
        "VeriTrueAI exception",
        message=exc.message,
        error_code=exc.error_code,
        path=request.url.path,
        method=request.method
    )
    
    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "message": exc.message,
                "type": "application_error",
                "error_code": exc.error_code
            }
        }
    )