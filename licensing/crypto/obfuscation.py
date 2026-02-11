"""
Obfuscated Storage
Triple-layer obfuscation for activation keys
"""
import os
import base64
import hmac
import hashlib
import ctypes
from pathlib import Path
from typing import Optional

class ObfuscatedStorage:
    """Store activation keys with maximum security"""
    
    def __init__(self):
        self.path = self._get_storage_path()
    
    def _get_storage_path(self) -> Path:
        """Get platform-specific storage path (constructed dynamically)"""
        if os.name == 'nt':  # Windows
            return self._get_windows_path()
        elif os.uname().sysname == 'Darwin':  # macOS
            return self._get_macos_path()
        else:  # Linux
            return self._get_linux_path()
    
    def _get_windows_path(self) -> Path:
        """Windows path using Win32 API (NO hardcoded strings!)"""
        # Get ProgramData folder via Win32 API
        CSIDL_COMMON_APPDATA = 0x0023
        buf = ctypes.create_unicode_buffer(260)
        ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_COMMON_APPDATA, None, 0, buf)
        base_path = Path(buf.value)
        
        # Construct subfolder name (obfuscated)
        part1 = bytes([0x57, 0x69, 0x6E]).decode()  # "Win"
        part2 = bytes([0x53, 0x79, 0x73]).decode()  # "Sys"
        subfolder = part1 + part2
        
        # Construct filename (obfuscated)
        name_bytes = [119, 105, 110, 115, 118, 99]  # "winsvc"
        filename = ''.join([chr(b) for b in name_bytes]) + '.dat'
        
        full_path = base_path / subfolder / filename
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        return full_path
    
    def _get_macos_path(self) -> Path:
        """macOS path"""
        base = Path.home() / "Library" / "Application Support"
        # Obfuscated folder name
        folder = ''.join([chr(b) for b in [46, 97, 105, 103, 101, 109]])  # ".aigem"
        filename = ''.join([chr(b) for b in [46, 97, 117, 116, 104]])  # ".auth"
        
        full_path = base / folder / filename
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        return full_path
    
    def _get_linux_path(self) -> Path:
        """Linux path"""
        base = Path.home() / ".config"
        folder = ''.join([chr(b) for b in [46, 97, 105, 103, 101, 109]])  # ".aigem"
        filename = ''.join([chr(b) for b in [46, 108, 105, 99]])  # ".lic"
        
        full_path = base / folder / filename
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        return full_path
    
    def _get_machine_key(self) -> bytes:
        """Get machine-specific key for obfuscation"""
        if os.name == 'nt':  # Windows
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography")
            guid, _ = winreg.QueryValueEx(key, "MachineGuid")
            return hashlib.sha256(guid.encode()).digest()
        else:
            # Use hostname + username as fallback
            import socket
            import getpass
            identifier = f"{socket.gethostname()}-{getpass.getuser()}"
            return hashlib.sha256(identifier.encode()).digest()
    
    def save_activation_key(self, activation_key: str):
        """Save activation key with triple-layer obfuscation"""
        system_key = self._get_machine_key()
        
        # Layer 1: XOR encryption
        key_bytes = activation_key.encode()
        xor_data = bytes([key_bytes[i] ^ system_key[i % len(system_key)] 
                          for i in range(len(key_bytes))])
        
        # Layer 2: Base64 encoding
        b64_data = base64.b64encode(xor_data)
        
        # Layer 3: HMAC signature
        signature = hmac.new(system_key, b64_data, hashlib.sha256).hexdigest()
        final_data = b64_data + b'::' + signature.encode()
        
        # Write as binary
        self.path.write_bytes(final_data)
        
        # Set hidden attribute on Windows
        if os.name == 'nt':
            import subprocess
            subprocess.run(['attrib', '+h', '+s', str(self.path)], 
                          shell=True, capture_output=True)
    
    def load_activation_key(self) -> Optional[str]:
        """Load and decrypt activation key"""
        if not self.path.exists():
            return None
        
        try:
            data = self.path.read_bytes()
            
            # Split data and signature
            b64_data, signature = data.rsplit(b'::', 1)
            
            # Verify signature
            system_key = self._get_machine_key()
            expected_sig = hmac.new(system_key, b64_data, hashlib.sha256).hexdigest().encode()
            
            if signature != expected_sig:
                # Tampered file!
                return None
            
            # Decode Base64
            xor_data = base64.b64decode(b64_data)
            
            # XOR decrypt
            key_bytes = bytes([xor_data[i] ^ system_key[i % len(system_key)] 
                              for i in range(len(xor_data))])
            
            return key_bytes.decode()
        
        except Exception as e:
            return None
