import os
import uuid
import shutil
from typing import Optional
from dataclasses import dataclass
from datetime import datetime
from fastapi import UploadFile

from app.core.config import settings


@dataclass
class FileInfo:
    """File information container."""
    file_id: str
    file_path: str
    original_filename: str
    content_type: str
    file_size: int
    upload_timestamp: datetime


class FileService:
    """Service for handling file uploads and management."""
    
    def __init__(self):
        self.upload_dir = settings.UPLOAD_DIR
        self._ensure_upload_directory()
    
    def _ensure_upload_directory(self):
        """Ensure upload directory exists."""
        os.makedirs(self.upload_dir, exist_ok=True)
    
    async def save_uploaded_file(self, file: UploadFile) -> FileInfo:
        """
        Save uploaded file to disk and return file information.
        """
        # Generate unique file ID
        file_id = str(uuid.uuid4())
        
        # Get file extension
        original_filename = file.filename or "unknown"
        file_extension = os.path.splitext(original_filename)[1]
        
        # Create unique filename
        unique_filename = f"{file_id}{file_extension}"
        file_path = os.path.join(self.upload_dir, unique_filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
            file_size = len(content)
        
        # Create file info
        file_info = FileInfo(
            file_id=file_id,
            file_path=file_path,
            original_filename=original_filename,
            content_type=file.content_type or "application/octet-stream",
            file_size=file_size,
            upload_timestamp=datetime.now()
        )
        
        # Store file metadata (in real implementation, this would go to database)
        await self._store_file_metadata(file_info)
        
        return file_info
    
    async def delete_file(self, file_id: str) -> bool:
        """
        Delete file by ID.
        """
        try:
            file_info = await self.get_file_info(file_id)
            if file_info and os.path.exists(file_info.file_path):
                os.remove(file_info.file_path)
                await self._delete_file_metadata(file_id)
                return True
            return False
        except Exception as e:
            print(f"Error deleting file {file_id}: {e}")
            return False
    
    async def get_file_info(self, file_id: str) -> Optional[FileInfo]:
        """
        Get file information by ID.
        """
        # In real implementation, this would query database
        # For now, we'll check if file exists and return mock info
        file_pattern = os.path.join(self.upload_dir, f"{file_id}.*")
        import glob
        
        matching_files = glob.glob(file_pattern)
        if matching_files:
            file_path = matching_files[0]
            if os.path.exists(file_path):
                stat = os.stat(file_path)
                return FileInfo(
                    file_id=file_id,
                    file_path=file_path,
                    original_filename=os.path.basename(file_path),
                    content_type="application/octet-stream",  # Would be stored in metadata
                    file_size=stat.st_size,
                    upload_timestamp=datetime.fromtimestamp(stat.st_ctime)
                )
        return None
    
    async def _store_file_metadata(self, file_info: FileInfo):
        """
        Store file metadata (placeholder for database storage).
        """
        # In real implementation, store in database
        print(f"Storing metadata for file {file_info.file_id}")
    
    async def _delete_file_metadata(self, file_id: str):
        """
        Delete file metadata (placeholder for database deletion).
        """
        # In real implementation, delete from database
        print(f"Deleting metadata for file {file_id}")
    
    def get_file_url(self, file_id: str) -> Optional[str]:
        """
        Get URL for accessing uploaded file.
        """
        file_info = self.get_file_info(file_id)
        if file_info:
            return f"/uploads/{os.path.basename(file_info.file_path)}"
        return None