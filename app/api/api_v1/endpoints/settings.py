from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Query

from app.schemas.models import UserSettings
from app.services.settings_service import SettingsService

router = APIRouter()


async def get_settings_service() -> SettingsService:
    """Dependency to get settings service."""
    return SettingsService()


@router.get("/{user_id}", response_model=UserSettings)
async def get_user_settings(
    user_id: str,
    settings_service: SettingsService = Depends(get_settings_service)
) -> UserSettings:
    """
    Get user settings and preferences.
    
    Returns all user configuration and preferences.
    """
    try:
        settings = await settings_service.get_user_settings(user_id)
        
        if not settings:
            # Return default settings if user doesn't have any
            settings = UserSettings(
                user_id=user_id,
                preferences={
                    "default_confidence_threshold": 0.7,
                    "preferred_source_types": ["academic", "news", "fact_check"],
                    "max_sources_per_analysis": 10,
                    "enable_batch_processing": True
                },
                notification_settings={
                    "email_analysis_complete": True,
                    "email_daily_summary": False,
                    "email_system_updates": True
                }
            )
            # Save default settings
            await settings_service.save_user_settings(settings)
            
        return settings
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get settings: {str(e)}")


@router.put("/{user_id}", response_model=UserSettings)
async def update_user_settings(
    user_id: str,
    settings: UserSettings,
    settings_service: SettingsService = Depends(get_settings_service)
) -> UserSettings:
    """
    Update user settings and preferences.
    
    Updates and returns the modified user settings.
    """
    try:
        # Ensure user_id matches
        settings.user_id = user_id
        
        updated_settings = await settings_service.save_user_settings(settings)
        
        return updated_settings
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update settings: {str(e)}")


@router.patch("/{user_id}/preferences")
async def update_user_preferences(
    user_id: str,
    preferences: Dict[str, Any],
    settings_service: SettingsService = Depends(get_settings_service)
):
    """
    Update specific user preferences.
    
    Allows partial updates to user preferences without affecting other settings.
    """
    try:
        updated_settings = await settings_service.update_preferences(user_id, preferences)
        
        if not updated_settings:
            raise HTTPException(status_code=404, detail="User settings not found")
            
        return {"message": "Preferences updated successfully", "preferences": updated_settings.preferences}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update preferences: {str(e)}")


@router.patch("/{user_id}/notifications")
async def update_notification_settings(
    user_id: str,
    notification_settings: Dict[str, bool],
    settings_service: SettingsService = Depends(get_settings_service)
):
    """
    Update user notification settings.
    
    Controls which notifications the user receives.
    """
    try:
        updated_settings = await settings_service.update_notification_settings(
            user_id, notification_settings
        )
        
        if not updated_settings:
            raise HTTPException(status_code=404, detail="User settings not found")
            
        return {
            "message": "Notification settings updated successfully",
            "notification_settings": updated_settings.notification_settings
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update notifications: {str(e)}")


@router.delete("/{user_id}")
async def delete_user_settings(
    user_id: str,
    settings_service: SettingsService = Depends(get_settings_service)
):
    """
    Delete all user settings and reset to defaults.
    """
    try:
        success = await settings_service.delete_user_settings(user_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="User settings not found")
            
        return {"message": "User settings deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete settings: {str(e)}")


@router.get("/")
async def get_system_settings(
    settings_service: SettingsService = Depends(get_settings_service)
):
    """
    Get system-wide settings and configuration.
    
    Returns global system configuration that affects all users.
    """
    try:
        system_settings = await settings_service.get_system_settings()
        
        return system_settings
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get system settings: {str(e)}")


@router.put("/system")
async def update_system_settings(
    settings: Dict[str, Any],
    settings_service: SettingsService = Depends(get_settings_service)
):
    """
    Update system-wide settings.
    
    Requires admin privileges (in a real implementation).
    """
    try:
        updated_settings = await settings_service.update_system_settings(settings)
        
        return {
            "message": "System settings updated successfully",
            "settings": updated_settings
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update system settings: {str(e)}")


@router.get("/{user_id}/export")
async def export_user_settings(
    user_id: str,
    settings_service: SettingsService = Depends(get_settings_service)
):
    """
    Export user settings for backup or migration.
    """
    try:
        settings = await settings_service.get_user_settings(user_id)
        
        if not settings:
            raise HTTPException(status_code=404, detail="User settings not found")
            
        return {
            "export_timestamp": "2024-01-01T00:00:00Z",  # Current timestamp in real implementation
            "user_settings": settings.dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export settings: {str(e)}")


@router.post("/{user_id}/import")
async def import_user_settings(
    user_id: str,
    settings_data: Dict[str, Any],
    settings_service: SettingsService = Depends(get_settings_service)
):
    """
    Import user settings from backup.
    """
    try:
        # Validate and create settings object
        user_settings_data = settings_data.get("user_settings", {})
        user_settings_data["user_id"] = user_id  # Ensure correct user_id
        
        settings = UserSettings(**user_settings_data)
        
        imported_settings = await settings_service.save_user_settings(settings)
        
        return {
            "message": "Settings imported successfully",
            "settings": imported_settings.dict()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to import settings: {str(e)}")