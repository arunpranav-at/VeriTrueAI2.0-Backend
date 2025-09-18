from typing import Dict, Any, Optional

from app.schemas.models import UserSettings


class SettingsService:
    """Service for managing user and system settings."""
    
    def __init__(self):
        # In real implementation, this would connect to database
        self._settings_storage = {}  # Mock storage
        self._system_settings = {
            "max_file_size_mb": 50,
            "max_batch_size": 10,
            "default_confidence_threshold": 0.7,
            "supported_file_types": ["jpg", "jpeg", "png", "gif", "webp", "mp4", "avi", "mov", "mkv"],
            "api_rate_limits": {
                "analyses_per_hour": 100,
                "uploads_per_hour": 50
            },
            "llm_settings": {
                "model": "gpt-3.5-turbo",
                "temperature": 0.3,
                "max_tokens": 1000
            },
            "search_settings": {
                "max_sources_per_query": 20,
                "default_source_limit": 10,
                "credibility_threshold": 0.5
            }
        }
    
    async def get_user_settings(self, user_id: str) -> Optional[UserSettings]:
        """
        Get user settings by ID.
        """
        return self._settings_storage.get(user_id)
    
    async def save_user_settings(self, settings: UserSettings) -> UserSettings:
        """
        Save user settings.
        """
        # Validate settings
        validated_settings = self._validate_user_settings(settings)
        
        # Store settings
        self._settings_storage[settings.user_id] = validated_settings
        
        return validated_settings
    
    async def update_preferences(
        self, 
        user_id: str, 
        preferences: Dict[str, Any]
    ) -> Optional[UserSettings]:
        """
        Update specific user preferences.
        """
        current_settings = await self.get_user_settings(user_id)
        
        if not current_settings:
            # Create new settings with provided preferences
            current_settings = UserSettings(
                user_id=user_id,
                preferences=preferences
            )
        else:
            # Update existing preferences
            current_settings.preferences.update(preferences)
        
        return await self.save_user_settings(current_settings)
    
    async def update_notification_settings(
        self, 
        user_id: str, 
        notification_settings: Dict[str, bool]
    ) -> Optional[UserSettings]:
        """
        Update user notification settings.
        """
        current_settings = await self.get_user_settings(user_id)
        
        if not current_settings:
            # Create new settings with provided notification settings
            current_settings = UserSettings(
                user_id=user_id,
                notification_settings=notification_settings
            )
        else:
            # Update existing notification settings
            current_settings.notification_settings.update(notification_settings)
        
        return await self.save_user_settings(current_settings)
    
    async def delete_user_settings(self, user_id: str) -> bool:
        """
        Delete user settings.
        """
        if user_id in self._settings_storage:
            del self._settings_storage[user_id]
            return True
        return False
    
    async def get_system_settings(self) -> Dict[str, Any]:
        """
        Get system-wide settings.
        """
        return self._system_settings.copy()
    
    async def update_system_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update system-wide settings.
        """
        # Validate and merge with existing settings
        validated_settings = self._validate_system_settings(settings)
        self._system_settings.update(validated_settings)
        
        return self._system_settings.copy()
    
    def _validate_user_settings(self, settings: UserSettings) -> UserSettings:
        """
        Validate user settings and apply defaults.
        """
        # Apply default preferences if not provided
        default_preferences = {
            "default_confidence_threshold": 0.7,
            "preferred_source_types": ["academic", "news", "fact_check"],
            "max_sources_per_analysis": 10,
            "enable_batch_processing": True,
            "auto_save_history": True,
            "preferred_language": "en",
            "theme": "light"
        }
        
        # Merge with provided preferences
        validated_preferences = default_preferences.copy()
        validated_preferences.update(settings.preferences)
        
        # Validate specific values
        if validated_preferences.get("default_confidence_threshold"):
            threshold = validated_preferences["default_confidence_threshold"]
            if not (0.0 <= threshold <= 1.0):
                validated_preferences["default_confidence_threshold"] = 0.7
        
        if validated_preferences.get("max_sources_per_analysis"):
            max_sources = validated_preferences["max_sources_per_analysis"]
            if not (1 <= max_sources <= 50):
                validated_preferences["max_sources_per_analysis"] = 10
        
        # Apply default notification settings if not provided
        default_notifications = {
            "email_analysis_complete": True,
            "email_daily_summary": False,
            "email_system_updates": True,
            "email_security_alerts": True,
            "push_analysis_complete": False,
            "push_daily_summary": False
        }
        
        validated_notifications = default_notifications.copy()
        validated_notifications.update(settings.notification_settings)
        
        # Create validated settings
        return UserSettings(
            user_id=settings.user_id,
            preferences=validated_preferences,
            notification_settings=validated_notifications,
            analysis_history_retention=settings.analysis_history_retention
        )
    
    def _validate_system_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate system settings.
        """
        validated = {}
        
        # Validate max file size
        if "max_file_size_mb" in settings:
            size = settings["max_file_size_mb"]
            if isinstance(size, (int, float)) and 1 <= size <= 500:
                validated["max_file_size_mb"] = size
        
        # Validate batch size
        if "max_batch_size" in settings:
            batch_size = settings["max_batch_size"]
            if isinstance(batch_size, int) and 1 <= batch_size <= 100:
                validated["max_batch_size"] = batch_size
        
        # Validate confidence threshold
        if "default_confidence_threshold" in settings:
            threshold = settings["default_confidence_threshold"]
            if isinstance(threshold, (int, float)) and 0.0 <= threshold <= 1.0:
                validated["default_confidence_threshold"] = threshold
        
        # Validate supported file types
        if "supported_file_types" in settings:
            file_types = settings["supported_file_types"]
            if isinstance(file_types, list):
                validated["supported_file_types"] = file_types
        
        # Validate API rate limits
        if "api_rate_limits" in settings:
            limits = settings["api_rate_limits"]
            if isinstance(limits, dict):
                validated_limits = {}
                if "analyses_per_hour" in limits:
                    rate = limits["analyses_per_hour"]
                    if isinstance(rate, int) and rate > 0:
                        validated_limits["analyses_per_hour"] = rate
                
                if "uploads_per_hour" in limits:
                    rate = limits["uploads_per_hour"]
                    if isinstance(rate, int) and rate > 0:
                        validated_limits["uploads_per_hour"] = rate
                
                if validated_limits:
                    validated["api_rate_limits"] = validated_limits
        
        # Validate LLM settings
        if "llm_settings" in settings:
            llm_settings = settings["llm_settings"]
            if isinstance(llm_settings, dict):
                validated_llm = {}
                
                if "model" in llm_settings:
                    model = llm_settings["model"]
                    if isinstance(model, str):
                        validated_llm["model"] = model
                
                if "temperature" in llm_settings:
                    temp = llm_settings["temperature"]
                    if isinstance(temp, (int, float)) and 0.0 <= temp <= 2.0:
                        validated_llm["temperature"] = temp
                
                if "max_tokens" in llm_settings:
                    tokens = llm_settings["max_tokens"]
                    if isinstance(tokens, int) and 1 <= tokens <= 4000:
                        validated_llm["max_tokens"] = tokens
                
                if validated_llm:
                    validated["llm_settings"] = validated_llm
        
        # Validate search settings
        if "search_settings" in settings:
            search_settings = settings["search_settings"]
            if isinstance(search_settings, dict):
                validated_search = {}
                
                if "max_sources_per_query" in search_settings:
                    max_sources = search_settings["max_sources_per_query"]
                    if isinstance(max_sources, int) and 1 <= max_sources <= 100:
                        validated_search["max_sources_per_query"] = max_sources
                
                if "default_source_limit" in search_settings:
                    limit = search_settings["default_source_limit"]
                    if isinstance(limit, int) and 1 <= limit <= 50:
                        validated_search["default_source_limit"] = limit
                
                if "credibility_threshold" in search_settings:
                    threshold = search_settings["credibility_threshold"]
                    if isinstance(threshold, (int, float)) and 0.0 <= threshold <= 1.0:
                        validated_search["credibility_threshold"] = threshold
                
                if validated_search:
                    validated["search_settings"] = validated_search
        
        return validated