import os
import uuid
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.schemas.models import MediaType
from app.services.file_service import FileService
from app.core.config import settings

router = APIRouter()


async def get_file_service() -> FileService:
    """Dependency to get file service."""
    return FileService()


@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    file_service: FileService = Depends(get_file_service)
) -> JSONResponse:
    """
    Upload a file (image or video) for analysis.
    
    Returns file information and prepared analysis request.
    """
    try:
        # Validate file type
        if not file.content_type:
            raise HTTPException(status_code=400, detail="File type could not be determined")
            
        # Check if file type is supported
        supported_types = {
            "image/jpeg", "image/png", "image/gif", "image/webp",
            "video/mp4", "video/avi", "video/mov", "video/mkv"
        }
        
        if file.content_type not in supported_types:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type: {file.content_type}"
            )
        
        # Validate file size
        file_size = 0
        content = await file.read()
        file_size = len(content)
        
        max_size = 50 * 1024 * 1024  # 50MB
        if file_size > max_size:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size is {max_size // (1024 * 1024)}MB"
            )
        
        # Reset file pointer
        await file.seek(0)
        
        # Save file
        file_info = await file_service.save_uploaded_file(file)
        
        # Determine media type
        media_type = MediaType.IMAGE if file.content_type.startswith("image/") else MediaType.VIDEO
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "File uploaded successfully",
                "file_id": file_info.file_id,
                "file_path": file_info.file_path,
                "media_type": media_type.value,
                "file_size": file_size,
                "content_type": file.content_type,
                "analysis_ready": True
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.post("/multiple")
async def upload_multiple_files(
    files: List[UploadFile] = File(...),
    file_service: FileService = Depends(get_file_service)
) -> JSONResponse:
    """
    Upload multiple files for batch analysis.
    
    Maximum 5 files per request.
    """
    if len(files) > 5:
        raise HTTPException(status_code=400, detail="Maximum 5 files per request")
    
    results = []
    errors = []
    
    for file in files:
        try:
            # Reuse single file upload logic
            response = await upload_file(file, file_service)
            results.append(response.body.decode())
        except HTTPException as e:
            errors.append({
                "filename": file.filename,
                "error": e.detail
            })
        except Exception as e:
            errors.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    return JSONResponse(
        status_code=200 if not errors else 207,  # 207 = Multi-Status
        content={
            "successful_uploads": len(results),
            "failed_uploads": len(errors),
            "results": results,
            "errors": errors
        }
    )


@router.delete("/{file_id}")
async def delete_file(
    file_id: str,
    file_service: FileService = Depends(get_file_service)
) -> JSONResponse:
    """
    Delete an uploaded file.
    """
    try:
        success = await file_service.delete_file(file_id)
        if success:
            return JSONResponse(
                status_code=200,
                content={"message": "File deleted successfully"}
            )
        else:
            raise HTTPException(status_code=404, detail="File not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deletion failed: {str(e)}")


@router.get("/{file_id}/info")
async def get_file_info(
    file_id: str,
    file_service: FileService = Depends(get_file_service)
) -> JSONResponse:
    """
    Get information about an uploaded file.
    """
    try:
        file_info = await file_service.get_file_info(file_id)
        if file_info:
            return JSONResponse(
                status_code=200,
                content=file_info.dict()
            )
        else:
            raise HTTPException(status_code=404, detail="File not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get file info: {str(e)}")