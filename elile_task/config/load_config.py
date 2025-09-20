"""
Configuration loader for the OMANI Therapist Voice Assistant
Loads configuration from config.yaml and provides easy access to settings
"""

import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ConfigurationError(Exception):
    """Custom exception for configuration related errors"""
    pass

class Config:
    """Configuration class that provides structured access to config values"""
    
    def __init__(self, config_data: Dict[str, Any]):
        self._data = config_data
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation (e.g., 'livekit.api_key')"""
        keys = key.split('.')
        value = self._data
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_required(self, key: str) -> Any:
        """Get required configuration value, raise error if not found"""
        value = self.get(key)
        if value is None or value == "":
            raise ConfigurationError(f"Required configuration key '{key}' is missing or empty")
        return value
    
    @property
    def livekit(self) -> Dict[str, str]:
        """Get LiveKit configuration"""
        return self._data.get('livekit', {})
    
    @property
    def ai_models(self) -> Dict[str, str]:
        """Get AI models configuration"""
        return self._data.get('ai_models', {})
    
    @property
    def elevenlabs(self) -> Dict[str, Any]:
        """Get ElevenLabs TTS configuration"""
        return self._data.get('elevenlabs', {})
    
    @property
    def deepgram(self) -> Dict[str, Any]:
        """Get Deepgram STT configuration"""
        return self._data.get('deepgram', {})
    
    @property
    def speech_services(self) -> Dict[str, Any]:
        """Get additional speech services configuration"""
        return self._data.get('speech_services', {})
    
    @property
    def integrations(self) -> Dict[str, str]:
        """Get integrations configuration"""
        return self._data.get('integrations', {})
    
    @property
    def raw_data(self) -> Dict[str, Any]:
        """Get raw configuration data"""
        return self._data

def find_config_file() -> Path:
    """Find config.yaml file in project root directory (outside config folder)"""
    # Get the parent directory of the config folder (project root)
    config_dir = Path(__file__).parent  # This is the config directory
    project_root = config_dir.parent     # This is the project root
    config_path = project_root / "config.yaml"
    
    if config_path.exists():
        return config_path
    
    # Fallback: Check current working directory
    current_dir = Path.cwd()
    config_path = current_dir / "config.yaml"
    
    if config_path.exists():
        return config_path
    
    # Fallback: Check parent directories
    for parent in current_dir.parents:
        config_path = parent / "config.yaml"
        if config_path.exists():
            return config_path
    
    raise ConfigurationError(
        f"config.yaml file not found. Expected locations:\n"
        f"  - {project_root / 'config.yaml'}\n"
        f"  - {current_dir / 'config.yaml'}\n"
        f"Please ensure config.yaml is in the project root directory."
    )

def load_configuration() -> Config:
    """Load configuration from config.yaml file"""
    try:
        config_path = find_config_file()
        logger.info(f"Loading configuration from: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as file:
            config_data = yaml.safe_load(file)
        
        if not config_data:
            raise ConfigurationError("Configuration file is empty or invalid")
        
        return Config(config_data)
    
    except yaml.YAMLError as e:
        raise ConfigurationError(f"Error parsing YAML configuration: {e}")
    except FileNotFoundError:
        raise ConfigurationError("Configuration file config.yaml not found")
    except Exception as e:
        raise ConfigurationError(f"Unexpected error loading configuration: {e}")

def validate_required_keys(config: Config) -> None:
    """Validate that required configuration keys are present"""
    required_keys = [
        'livekit.url',
        'livekit.api_key', 
        'livekit.api_secret',
        'ai_models.openai_api_key'
    ]
    
    missing_keys = []
    for key in required_keys:
        try:
            config.get_required(key)
        except ConfigurationError:
            missing_keys.append(key)
    
    if missing_keys:
        logger.warning(f"Missing required configuration keys: {missing_keys}")
        logger.warning("Some features may not work properly without these keys")

# Global configuration instance
_global_config: Optional[Config] = None

def get_config() -> Config:
    """Get the global configuration instance (singleton pattern)"""
    global _global_config
    
    if _global_config is None:
        _global_config = load_configuration()
        validate_required_keys(_global_config)
    
    return _global_config

def reload_config() -> Config:
    """Reload configuration from file (useful for development)"""
    global _global_config
    _global_config = None
    return get_config()

# Environment variable fallback helper
def get_env_or_config(config: Config, config_key: str, env_key: str, default: str = "") -> str:
    """Get value from environment variable first, then config, then default"""
    env_value = os.getenv(env_key)
    if env_value:
        return env_value
    
    config_value = config.get(config_key, default)
    return config_value if config_value else default
