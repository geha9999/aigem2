"""
Triple-Layer Obfuscation for Activation Key Storage
"""
import os
import base64
import hmac
import hashlib
import platform
from pathlib import Path
from typing import Optional
import ctypes
from ctypes import wintypes

class ObfuscatedStorage:
    """Store activation key with triple-layer obfuscation"""
    
    def __init__(self):
        self.license_path = self._get_license_path()
    
    def _get_license_path(self) -> Path:
        """
        Construct file path dynamically (NO hardcoded paths!)
        Platform-specific implementation
        """
        system = platform.system()
        
        if system == "Windows":
            return self._get_path_windows()
        elif system == "Darwin":  # macOS
            return self._get_path_macos()
        else:  # Linux
            return self._get_path_linux()
    
    def _get_path_windows(self) -> Path:
        """Windows: Use Win32 API to construct path""" 
        # Get ProgramData folder via Win32 API
        CSIDL_COMMON_APPDATA = 0x0023
        buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_COMMON_APPDATA, None, 0, buf)
        base_path = Path(buf.value)
        
        # Obfuscated subfolder name (NOT plaintext "AIGEM2"!)
        part1 = bytes([0x57, 0x69, 0x6E]).decode()  # "Win"
        part2 = bytes([0x53, 0x79, 0x73]).decode()  # "Sys"
        subfolder = part1 + part2
        
        # Obfuscated filename
        name_bytes = [119, 105, 110, 115, 118, 99]  # "winsvc"
        filename = ''.join([chr(b) for b in name_bytes]) + '.dat'
        
        full_path = base_path / subfolder / filename
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        return full_path
    
    def _get_path_macos(self) -> Path:
        """macOS: ~/Library/Application Support/.aigem/.auth"""
        base = Path.home() / "Library" / "Application Support"
        # Obfuscated folder
        folder = '.' + ''.join([chr(c) for c in [97, 105, 103, 101, 109]])  # ".aigem"
        filename = '.' + ''.join([chr(c) for c in [97, 117, 116, 104]])  # ".auth"
        
        full_path = base / folder / filename
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        return full_path
    
    def _get_path_linux(self) -> Path:
        """Linux: ~/.config/.aigem/.license"""
        base = Path.home() / ".config"
        folder = '.' + ''.join([chr(c) for c in [97, 105, 103, 101, 109]])
        filename = '.' + ''.join([chr(c) for c in [108, 105, 99, 101, 110, 115, 101]])
        
        full_path = base / folder / filename
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        return full_path
    
    def _get_machine_guid(self) -> str:
        """Get machine-specific GUID for obfuscation key""" 
        system = platform.system()
        
        if system == "Windows":
            try:
                import winreg
                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE, 
                    r"SOFTWARE\Microsoft\Cryptography"
                )
                guid, _ = winreg.QueryValueEx(key, "MachineGuid")
                return guid
            except:
                pass
        
        # Fallback: use hostname
        return platform.node()
    
    def save_activation_key(self, activation_key: str):
        """
        Save with triple-layer obfuscation:
        1. XOR with machine-specific key
        2. Base64 encode
        3. HMAC signature
        """
        # Get system-specific key
        machine_guid = self._get_machine_guid()
        system_key = hashlib.sha256(machine_guid.encode()).digest()
        
        # Layer 1: XOR encryption
        key_bytes = activation_key.encode()
        xor_data = bytes([
            key_bytes[i % len(key_bytes)] ^ system_key[i % len(system_key)]
            for i in range(len(key_bytes))
        ])
        
        # Layer 2: Base64 encode
        b64_data = base64.b64encode(xor_data)
        
        # Layer 3: HMAC signature
        signature = hmac.new(system_key, b64_data, hashlib.sha256).hexdigest()
        final_data = b64_data + b'::' + signature.encode()
        
        # Write as binary
        self.license_path.write_bytes(final_data)
        
        # Set file attributes (Windows: hidden + system)
        if platform.system() == "Windows":
            try:
                import subprocess
                subprocess.run(
                    ['attrib', '+h', '+s', str(self.license_path)],
                    shell=True,
                    stderr=subprocess.DEVNULL
                )
            except:
                pass
    
    def load_activation_key(self) -> Optional[str]:
        """Load and decrypt activation key""" 
        if not self.license_path.exists():
            return None
        
        try:
            data = self.license_path.read_bytes()
            
            # Split data and signature
            b64_data, signature = data.rsplit(b'::', 1)
            
            # Verify signature
            machine_guid = self._get_machine_guid()
            system_key = hashlib.sha256(machine_guid.encode()).digest()
            expected_sig = hmac.new(
                system_key, 
                b64_data, 
                hashlib.sha256
            ).hexdigest().encode()
            
            if signature != expected_sig:
                raise ValueError("Activation file tampered!")
            
            # Decode Base64
            xor_data = base64.b64decode(b64_data)
            
            # XOR decrypt
            key_bytes = bytes([
                xor_data[i] ^ system_key[i % len(system_key)]
                for i in range(len(xor_data))
            ])
            
            return key_bytes.decode()
            
        except Exception as e:
            print(f"Load error: {e}")
            return None
