"""
AIGEM2 Configuration Manager
Loads settings from server API and local cache
"""
import os
import json
import httpx
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any

class AppConfig:
    """Application configuration with server sync"""
    
    API_BASE_URL = os.getenv("AIGEM2_API_URL", "https://aigem2.vercel.app/api")
    CACHE_DIR = Path.home() / ".aigem2" / "cache"
    CONFIG_CACHE_FILE = CACHE_DIR / "config.json"
    CACHE_VALIDITY_HOURS = 24
    
    def __init__(self):
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load config from cache or fetch from server"""
        
        # Try cache first
        if self.CONFIG_CACHE_FILE.exists():
            cache_data = json.loads(self.CONFIG_CACHE_FILE.read_text())
            cache_time = datetime.fromisoformat(cache_data.get("cached_at", "2000-01-01"))
            
            if datetime.utcnow() - cache_time < timedelta(hours=self.CACHE_VALIDITY_HOURS):
                return cache_data.get("config", self._default_config())
        
        # Fetch from server
        try:
            response = httpx.get(f"{self.API_BASE_URL}/config/pricing", timeout=5.0)
            if response.status_code == 200:
                config = response.json()
                self._save_cache(config)
                return config
        except:
            pass
        
        # Fallback to default
        return self._default_config()
    
    def _save_cache(self, config: Dict[str, Any]):
        """Save config to local cache""" 
        cache_data = {
            "cached_at": datetime.utcnow().isoformat(),
            "config": config
        }
        self.CONFIG_CACHE_FILE.write_text(json.dumps(cache_data, indent=2))
    
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration (offline fallback)""" 
        return {
            "tiers": {
                "FREE": {
                    "price_idr": 0,
                    "price_usd": 0,
                    "storage_limit_mb": 100,
                    "video_downloads_monthly": 3,
                    "features": {
                        "notes": True,
                        "basic_search": True,
                        "export_markdown": True
                    }
                },
                "STARTER": {
                    "price_idr": 99000,
                    "price_usd": 12,
                    "storage_limit_mb": 2000,
                    "video_downloads_monthly": -1,
                    "features": {
                        "notes": True,
                        "video_download": True,
                        "transcription": True,
                        "subtitles": True
                    }
                },
                "PRO": {
                    "price_idr": 299000,
                    "price_usd": 49,
                    "storage_limit_mb": -1,
                    "video_downloads_monthly": -1,
                    "features": {
                        "all_starter": True,
                        "semantic_search": True,
                        "local_ai": True,
                        "screen_recorder": True,
                        "pdf_export": True
                    }
                },
                "PREMIUM": {
                    "price_idr": 149000,
                    "price_usd": 19,
                    "billing_period": "monthly",
                    "storage_limit_mb": -1,
                    "ai_tokens_monthly": 30000,
                    "features": {
                        "all_pro": True,
                        "cloud_ai": True,
                        "content_repurposer": True,
                        "translation": True,
                        "priority_support": True
                    }
                }
            }
        }
    
    def get_tier_config(self, tier: str) -> Dict[str, Any]:
        """Get configuration for specific tier""" 
        return self._config.get("tiers", {}).get(tier, {})
    
    def refresh(self):
        """Force refresh config from server""" 
        if self.CONFIG_CACHE_FILE.exists():
            self.CONFIG_CACHE_FILE.unlink()
        self._config = self._load_config()