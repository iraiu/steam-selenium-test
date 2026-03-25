import json
from pathlib import Path


class ConfigReader:
    _config = None

    @classmethod
    def _load_config(cls):
        if cls._config is None:
            config_path = Path(__file__).resolve().parent.parent / "config.json"
            with open(config_path, encoding="utf-8") as file:
                cls._config = json.load(file)

    @classmethod
    def get(cls, key, default=None):
        cls._load_config()
        return cls._config.get(key, default)