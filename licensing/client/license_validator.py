"""
License Validator - Offline validation with JWT
"""
import jwt
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any
from .hardware_fingerprint import HardwareFingerprint
from ..crypto.obfuscation import ObfuscatedStorage

class LicenseValidator:
    """Validate license and activation keys"""
    
    CACHE_DIR = Path.home() / ".aigem2" / "cache"
    
    def __init__(self):
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self.storage = ObfuscatedStorage()
        self.hwid = HardwareFingerprint.generate()
    
    def validate_activation(self) -> Optional[str]:
        """
        Validate activation key stored locally
        Returns tier if valid, None if invalid/expired
        """
        activation_key = self.storage.load_activation_key()
        
        if not activation_key:
            return None
        
        try:
            # Decode JWT (no signature verification for offline use)
            payload = jwt.decode(
                activation_key, 
                options={"verify_signature": False}
            )
            
            tier = payload.get('tier')
            hwid = payload.get('hwid')
            issued = datetime.fromisoformat(payload.get('issued'))
            last_heartbeat = datetime.fromisoformat(
                payload.get('last_heartbeat', payload.get('issued'))
            )
            
            # Verify HWID matches
            if hwid != self.hwid:
                return None
            
            # Check offline grace period (30 days)
            days_since_heartbeat = (datetime.utcnow() - last_heartbeat).days
            
            if days_since_heartbeat > 30:
                return "REQUIRE_ONLINE"
            
            return tier
            
        except Exception as e:
            print(f"Validation error: {e}")
            return None
    
    def get_license_status(self) -> Dict[str, Any]:
        """Get detailed license status"""
        tier = self.validate_activation()
        
        if tier is None:
            return {
                "status": "NOT_ACTIVATED",
                "tier": "FREE",
                "message": "App not activated. Using FREE tier."
            }
        
        if tier == "REQUIRE_ONLINE":
            return {
                "status": "EXPIRED",
                "tier": "FREE",
                "message": "Offline grace period expired. Please connect to internet."
            }
        
        return {
            "status": "ACTIVE",
            "tier": tier,
            "message": f"{tier} tier activated"
        }

def check_license_validity() -> str:
    """Convenience function - returns tier string"""
    validator = LicenseValidator()
    status = validator.get_license_status()
    return status['tier']
