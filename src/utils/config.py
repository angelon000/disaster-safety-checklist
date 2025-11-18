"""
Configuration management for KCL Checklist System
"""
import json
import os
from pathlib import Path
from typing import Dict, Any


class Config:
    """설정 관리 클래스"""

    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config" / "settings.json"

        self.config_path = Path(config_path)
        self.settings = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """설정 파일 로드"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 기본 설정
            default_config = {
                "api_keys": {
                    "github": os.getenv("GITHUB_TOKEN", ""),
                    "semantic_scholar": "",  # 무료, API 키 불필요
                    "crossref": "",  # 무료, API 키 불필요
                    "public_data": os.getenv("PUBLIC_DATA_API_KEY", "")
                },
                "data_dir": "data",
                "output_dir": "output",
                "max_results_per_source": 10,
                "cache_duration_hours": 24,
                "web_search": {
                    "enabled": True,
                    "max_pages": 5,
                    "timeout": 10
                },
                "paper_search": {
                    "enabled": True,
                    "sources": ["semantic_scholar", "crossref", "arxiv"]
                },
                "tech_search": {
                    "enabled": True,
                    "github_min_stars": 10
                },
                "api_search": {
                    "enabled": True
                }
            }

            # 설정 파일 생성
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)

            return default_config

    def get(self, key: str, default: Any = None) -> Any:
        """설정값 가져오기 (점 표기법 지원)"""
        keys = key.split('.')
        value = self.settings

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """설정값 설정하기 (점 표기법 지원)"""
        keys = key.split('.')
        current = self.settings

        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]

        current[keys[-1]] = value

    def save(self) -> None:
        """설정을 파일에 저장"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, indent=2, ensure_ascii=False)


# 글로벌 설정 인스턴스
config = Config()
