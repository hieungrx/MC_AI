import os
import sys

# Default fallback configurations
DEFAULT_CONFIG = {
    "app": {
        "name": "AI_MC",
        "version": "0.1.0",
        "env": "development"
    },
    "logging": {
        "level": "INFO",
        "file_path": "logs/app.log",
        "max_bytes": 10485760,
        "backup_count": 5
    },
    "voice": {
        "provider": "edge-tts",
        "voice_name": "vi-VN-HoaiMyNeural",
        "speed": "+0%",
        "pitch": "+0Hz",
        "output_dir": "assets/audio"
    },
    "avatar": {
        "model_name": "wav2lip",
        "default_face": "assets/avatar/mc_default.png",
        "output_dir": "assets/video",
        "fps": 25
    },
    "streaming": {
        "obs_websocket": {
            "host": "localhost",
            "port": 4455,
            "password": "change_me"
        },
        "rtmp_url": "rtmp://localhost/live",
        "stream_key": "default_stream_key"
    },
    "automation": {
        "product_file": "configs/products.json",
        "loop_interval": 10
    }
}

class Config:
    def __init__(self, data=None):
        self._data = data or DEFAULT_CONFIG

    def get(self, key, default=None):
        """Get config value using dot notation, e.g., config.get('logging.level')"""
        parts = key.split('.')
        val = self._data
        for part in parts:
            if isinstance(val, dict) and part in val:
                val = val[part]
            else:
                return default
        return val

    @property
    def data(self):
        return self._data

def load_config(config_path="configs/default.yaml"):
    """
    Loads configuration from a YAML file. Fallbacks to DEFAULT_CONFIG if loading fails.
    """
    if not os.path.exists(config_path):
        print(f"Warning: Configuration file {config_path} not found. Using defaults.")
        return Config(DEFAULT_CONFIG)

    try:
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            # Simple merge with default config to ensure all keys exist
            merged = merge_configs(DEFAULT_CONFIG, data or {})
            return Config(merged)
    except ImportError:
        print("Warning: PyYAML is not installed. To parse YAML files, install PyYAML. Using defaults.")
        return Config(DEFAULT_CONFIG)
    except Exception as e:
        print(f"Warning: Failed to load config from {config_path} ({e}). Using defaults.")
        return Config(DEFAULT_CONFIG)

def merge_configs(default, override):
    """
    Recursively merges override dictionary into default dictionary.
    """
    result = default.copy()
    for key, val in override.items():
        if isinstance(val, dict) and key in result and isinstance(result[key], dict):
            result[key] = merge_configs(result[key], val)
        else:
            result[key] = val
    return result

# Global config instance
config = load_config()
