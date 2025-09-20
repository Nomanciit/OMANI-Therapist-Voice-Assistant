"""
Configuration package for the OMANI Therapist Voice Assistant
"""

from .load_config import load_configuration, get_config, Config, ConfigurationError

# Make configuration easily accessible
config = get_config()

__all__ = ['load_configuration', 'get_config', 'config', 'Config', 'ConfigurationError']
