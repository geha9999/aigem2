"""
AIGEM2 Main Application
Streamlit-based UI with lazy module loading
"""
import streamlit as st
from pathlib import Path
import sys

# Add project root to path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config import AppConfig
from ui.theme import apply_theme, toggle_theme
from i18n.loader import get_text, set_language
from modules.plugin_manager import PluginManager


class MainApp:
    """Main application controller""" 
    
def __init__(self, config: AppConfig, license_tier: str):
        self.config = config
        self.license_tier = license_tier
        self.plugin_manager = PluginManager(config, license_tier)
        
        # Initialize session state
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'dashboard'
        if 'theme' not in st.session_state:
            st.session_state.theme = 'dark'
        if 'language' not in st.session_state:
            st.session_state.language = 'en'
    
def run(self):
        """Main application loop"""        
        # Apply theme
        apply_theme(st.session_state.theme)
        
        # Render header
        self._render_header()
        
        # Render sidebar
        selected_page = self._render_sidebar()
        
        # Render main content
        self._render_content(selected_page)
    
def _render_header(self):
        """Render top header bar"""        
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        
        with col1:
            st.markdown("# 💎 AIGEM2")
        
        with col2:
            # Theme toggle
            theme_icon = "🌙" if st.session_state.theme == "dark" else "☀️"
            if st.button(theme_icon, key="theme_toggle"):
                st.session_state.theme = toggle_theme(st.session_state.theme)
                st.rerun()
        
        with col3:
            # Language selector
            lang = st.selectbox(
                "",
                options=["en", "id"],
                format_func=lambda x: "🇬🇧 EN" if x == "en" else "🇮🇩 ID",
                key="lang_select",
                label_visibility="collapsed"
            )
            if lang != st.session_state.language:
                st.session_state.language = lang
                set_language(lang)
                st.rerun()
        
        with col4:
            # Tier badge
            from ui.components.tier_badge import render_tier_badge
            render_tier_badge(self.license_tier)
        
        st.divider()
    
def _render_sidebar(self) -> str:
        """Render sidebar navigation"""        
        with st.sidebar:
            st.markdown("## " + get_text("navigation"))
            
            # Core modules (always available)
            pages = {
                "dashboard": {"icon": "🏠", "label": get_text("dashboard"), "tier": "FREE"},
                "knowledge_base": {"icon": "📚", "label": get_text("knowledge_base"), "tier": "FREE"},
            }
            
            # Conditional modules based on tier
            if self._check_tier_access("STARTER"):
                pages["video_downloader"] = {"icon": "🎥", "label": get_text("video_downloader"), "tier": "STARTER"}
                pages["transcription"] = {"icon": "🎙️", "label": get_text("transcription"), "tier": "STARTER"}
            
            if self._check_tier_access("PRO"):
                pages["ai_assistant"] = {"icon": "🤖", "label": get_text("ai_assistant"), "tier": "PRO"}
                pages["screen_recorder"] = {"icon": "🖥️", "label": get_text("screen_recorder"), "tier": "PRO"}
            
            if self._check_tier_access("PREMIUM"):
                pages["content_repurposer"] = {"icon": "✍️", "label": get_text("content_repurposer"), "tier": "PREMIUM"}
                pages["translation"] = {"icon": "🌍", "label": get_text("translation"), "tier": "PREMIUM"}
            
            # Render navigation buttons
            selected = None
            for page_id, page_info in pages.items():
                if st.button(
                    f"{page_info['icon']} {page_info['label']}", 
                    key=f"nav_{page_id}",
                    use_container_width=True
                ):
                    selected = page_id
            
            st.divider()
            
            # Settings & Tier Management
            if st.button("⚙️ " + get_text("settings"), key="nav_settings", use_container_width=True):
                selected = "settings"
            
            if st.button("💳 " + get_text("tier_management"), key="nav_tier", use_container_width=True):
                selected = "tier_management"
            
            return selected if selected else st.session_state.current_page
    
def _render_content(self, page: str):
        """Render main content area"""        
        st.session_state.current_page = page
        
        if page == "dashboard":
            from ui.pages.dashboard import render_dashboard
            render_dashboard(self.license_tier, self.config)
        
        elif page == "settings":
            from ui.pages.settings import render_settings
            render_settings(self.config)
        
        elif page == "tier_management":
            from ui.pages.tier_management import render_tier_management
            render_tier_management(self.license_tier, self.config)
        
        else:
            # Load plugin module
            self._load_plugin(page)
    
def _load_plugin(self, plugin_id: str):
        """Load and render plugin module"""        
        # Check tier access
        plugin_meta = self.plugin_manager.get_plugin_metadata(plugin_id)
        
        if not plugin_meta:
            st.error(f"Plugin '{plugin_id}' not found")
            return
        
        if not self._check_tier_access(plugin_meta.get("tier_required", "FREE")):
            st.warning(get_text("upgrade_required"))
            st.info(f"This feature requires {plugin_meta['tier_required']} tier or higher")
            
            if st.button("⬆️ Upgrade Now"):
                st.session_state.current_page = "tier_management"
                st.rerun()
            return
        
        # Load plugin with spinner
        with st.spinner(get_text("loading_module")):
            plugin = self.plugin_manager.load_plugin(plugin_id)
            
            if plugin:
                plugin.render_ui()
            else:
                st.error(get_text("module_load_failed"))
    
def _check_tier_access(self, required_tier: str) -> bool:
        """Check if current tier has access to required tier"""
        tier_hierarchy = ["FREE", "STARTER", "PRO", "PREMIUM"]
        
        try:
            current_index = tier_hierarchy.index(self.license_tier)
            required_index = tier_hierarchy.index(required_tier)
            return current_index >= required_index
        except ValueError:
            return False
