import os

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
        "fps": 25,
        "checkpoint_path": "checkpoints/wav2lip.pth"
    },
    "streaming": {
        "obs_websocket": {
            "host": "localhost",
            "port": 4455,
            "password": ""  # Set via OBS_PASSWORD environment variable
        },
        "rtmp_url": "rtmp://localhost/live",
        "stream_key": ""  # Set via STREAM_KEY environment variable
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

def _resolve_env_vars(data):
    """
    Recursively resolve environment variable placeholders in config values.
    Supports the format: ${ENV_VAR_NAME} or ${ENV_VAR_NAME:default_value}
    """
    if isinstance(data, dict):
        return {k: _resolve_env_vars(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [_resolve_env_vars(item) for item in data]
    elif isinstance(data, str) and data.startswith("${") and data.endswith("}"):
        inner = data[2:-1]
        if ":" in inner:
            env_key, default_val = inner.split(":", 1)
        else:
            env_key, default_val = inner, ""
        return os.environ.get(env_key, default_val)
    return data

def load_config(config_path="configs/default.yaml"):
    """
    Loads configuration from a YAML file. Fallbacks to DEFAULT_CONFIG if loading fails.
    Environment variable placeholders (${VAR_NAME} or ${VAR_NAME:default}) are resolved.
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
            # Resolve environment variable references
            resolved = _resolve_env_vars(merged)
            return Config(resolved)
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
