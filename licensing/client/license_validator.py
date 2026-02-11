"""
License Validator
Validates license offline and online
"""
import jwt
import httpx
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from pathlib import Path
from .hardware_fingerprint import HardwareFingerprint
from ..crypto.obfuscation import ObfuscatedStorage

class LicenseValidator:
    """Validate license keys and activation"""
    
    API_BASE_URL = "https://aigem2.vercel.app/api"
    
    def __init__(self):
        self.storage = ObfuscatedStorage()
        self.hw_fingerprint = HardwareFingerprint()
    
    def activate_license(self, license_key: str) -> Dict[str, Any]:
        """Activate license with server"""
        hwid = self.hw_fingerprint.generate()
        
        try:
            response = httpx.post(
                f"{self.API_BASE_URL}/license/activate",
                json={
                    "license_key": license_key,
                    "hardware_fingerprint": hwid,
                    "device_info": {
                        "os": self.hw_fingerprint.get_os_info(),
                        "cpu": self.hw_fingerprint.get_cpu_id()
                    }
                },
                timeout=10.0
            )
            
            if response.status_code == 200:
                data = response.json()
                activation_key = data["activation_key"]
                
                # Save activation key (obfuscated)
                self.storage.save_activation_key(activation_key)
                
                return {
                    "success": True,
                    "tier": data["tier"],
                    "message": "License activated successfully!"
                }
            else:
                return {
                    "success": False,
                    "message": response.json().get("error", "Activation failed")
                }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Network error: {str(e)}"
            }
    
    def validate_offline(self) -> Optional[str]:
        """Validate license offline (from local storage)"""
        activation_key = self.storage.load_activation_key()
        
        if not activation_key:
            return None
        
        try:
            # Decode JWT (no signature verification for offline)
            payload = jwt.decode(activation_key, options={"verify_signature": False})
            
            tier = payload.get("tier", "FREE")
            issued = datetime.fromisoformat(payload["issued"])
            last_heartbeat = datetime.fromisoformat(payload.get("last_heartbeat", payload["issued"]))
            
            # Check offline grace period (30 days)
            days_since_heartbeat = (datetime.utcnow() - last_heartbeat).days
            
            if days_since_heartbeat > 30:
                return "REQUIRE_ONLINE"
            
            return tier
        
        except Exception as e:
            return None
    
    def heartbeat(self):
        """Send heartbeat to server (background task)"""
        activation_key = self.storage.load_activation_key()
        
        if not activation_key:
            return
        
        try:
            response = httpx.post(
                f"{self.API_BASE_URL}/license/heartbeat",
                json={"activation_key": activation_key},
                timeout=5.0
            )
            
            if response.status_code == 200:
                # Update local activation key with new heartbeat timestamp
                new_key = response.json()["activation_key"]
                self.storage.save_activation_key(new_key)
        
        except:
            # Silently fail (offline is OK)
            pass

def check_license_validity() -> str:
    """Main function to check license status"""
    validator = LicenseValidator()
    
    tier = validator.validate_offline()
    
    if tier is None:
        return "NOT_ACTIVATED"
    
    if tier == "REQUIRE_ONLINE":
        # TODO: Show modal to user asking to go online
        return "FREE"  # Fallback to FREE temporarily
    
    # Schedule heartbeat if needed (every 7 days)
    # TODO: Implement background task
    
    return tier
