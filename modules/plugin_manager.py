"""
Plugin Manager
Dynamic module loading system
"""
import json
import importlib
from pathlib import Path
from typing import Dict, Optional, Any

class PluginManager:
    """Manage plugin modules with lazy loading"""
    
    def __init__(self, config, license_tier: str):
        self.config = config
        self.license_tier = license_tier
        self.loaded_plugins = {}
        self.plugin_registry = {}
        self._scan_plugins()
    
    def _scan_plugins(self):
        """Scan modules directory for available plugins"""
        modules_dir = Path(__file__).parent
        
        for plugin_dir in modules_dir.iterdir():
            if plugin_dir.is_dir() and not plugin_dir.name.startswith('_'):
                plugin_json = plugin_dir / "plugin.json"
                
                if plugin_json.exists():
                    with open(plugin_json, 'r') as f:
                        metadata = json.load(f)
                        self.plugin_registry[plugin_dir.name] = {
                            "path": plugin_dir,
                            "metadata": metadata
                        }
    
    def get_plugin_metadata(self, plugin_id: str) -> Optional[Dict[str, Any]]:
        """Get plugin metadata"""
        plugin_info = self.plugin_registry.get(plugin_id)
        return plugin_info["metadata"] if plugin_info else None
    
    def load_plugin(self, plugin_id: str):
        """Load plugin module dynamically"""
        
        # Check if already loaded
        if plugin_id in self.loaded_plugins:
            return self.loaded_plugins[plugin_id]
        
        # Get plugin info
        plugin_info = self.plugin_registry.get(plugin_id)
        if not plugin_info:
            return None
        
        metadata = plugin_info["metadata"]
        
        # Check tier requirement
        tier_required = metadata.get("tier_required", "FREE")
        if not self._check_tier_access(tier_required):
            return None
        
        # Dynamic import
        try:
            entry_point = metadata.get("entry_point", "ui.py:PluginUI")
            module_name, class_name = entry_point.split(":")
            
            module_path = f"modules.{plugin_id}.{module_name.replace('.py', '')}"
            module = importlib.import_module(module_path)
            
            plugin_class = getattr(module, class_name)
            plugin_instance = plugin_class(self.config, self.license_tier)
            
            # Cache loaded plugin
            self.loaded_plugins[plugin_id] = plugin_instance
            
            return plugin_instance
            
        except Exception as e:
            print(f"Failed to load plugin {plugin_id}: {e}")
            return None
    
    def unload_plugin(self, plugin_id: str):
        """Unload plugin from memory"""
        if plugin_id in self.loaded_plugins:
            plugin = self.loaded_plugins[plugin_id]
            if hasattr(plugin, 'cleanup'):
                plugin.cleanup()
            del self.loaded_plugins[plugin_id]
    
    def _check_tier_access(self, required_tier: str) -> bool:
        """Check tier access"""
        tier_hierarchy = ["FREE", "STARTER", "PRO", "PREMIUM"]
        
        try:
            current_index = tier_hierarchy.index(self.license_tier)
            required_index = tier_hierarchy.index(required_tier)
            return current_index >= required_index
        except ValueError:
            return False