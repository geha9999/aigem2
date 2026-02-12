"""
AIGEM2 Main Application Controller
Handles navigation, state management, and module loading
"""
import streamlit as st
from typing import Optional
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import AppConfig
from ui.theme import ThemeManager
from i18n.loader import I18nLoader
from modules.plugin_manager import PluginManager

class MainApp:
    """Main application controller"""
    
    def __init__(self, config: AppConfig, license_tier: str):
        self.config = config
        self.license_tier = license_tier
        self.theme = ThemeManager()
        self.i18n = I18nLoader()
        self.plugin_manager = PluginManager(config, license_tier)
        
        # Initialize session state
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'dashboard'
        if 'language' not in st.session_state:
            st.session_state.language = 'en'
        if 'theme_mode' not in st.session_state:
            st.session_state.theme_mode = 'dark'
    
    def run(self):
        """Main application loop"""
        
        # Apply theme
        self.theme.apply(st.session_state.theme_mode)
        
        # Load translations
        t = self.i18n.load(st.session_state.language)
        
        # Render header
        self._render_header(t)
        
        # Render sidebar
        self._render_sidebar(t)
        
        # Render main content
        self._render_content(t)
    
    def _render_header(self, t):
        """Render top header bar"""
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        
        with col1:
            st.markdown("# 💎 AIGEM2")
        
        with col2:
            # Theme toggle
            theme_icon = "🌙" if st.session_state.theme_mode == "dark" else "☀️"
            if st.button(theme_icon, key="theme_toggle"):
                st.session_state.theme_mode = "light" if st.session_state.theme_mode == "dark" else "dark"
                st.rerun()
        
        with col3:
            # Language selector
            lang = st.selectbox(
                "Lang",
                options=["en", "id"],
                format_func=lambda x: "🇬🇧 EN" if x == "en" else "🇮🇩 ID",
                key="language_selector",
                label_visibility="collapsed"
            )
            if lang != st.session_state.language:
                st.session_state.language = lang
                st.rerun()
        
        with col4:
            # Tier badge
            self._render_tier_badge()
        
        st.divider()
    
    def _render_tier_badge(self):
        """Render tier badge"""
        tier_colors = {
            "FREE": "#6B7280",
            "STARTER": "#3B82F6",
            "PRO": "#10B981",
            "PREMIUM": "#F59E0B"
        }
        
        color = tier_colors.get(self.license_tier, "#6B7280")
        
        st.markdown(f"""
        <div style="
            background: {color}20;
            border: 1px solid {color};
            border-radius: 6px;
            padding: 4px 12px;
            text-align: center;
            font-size: 12px;
            font-weight: 600;
            color: {color};
        }">
            {self.license_tier}
        </div>
        """, unsafe_allow_html=True)
    
    def _render_sidebar(self, t):
        """Render sidebar navigation"""
        with st.sidebar:
            st.markdown("### 📚 " + t.get("modules", "Modules"))
            
            # Get available plugins
            plugins = self.plugin_manager.get_available_plugins()
            
            for plugin_id, plugin_info in plugins.items():
                # Check if user has access
                is_locked = not self.plugin_manager.can_access_plugin(plugin_id)
                
                # Render menu item
                icon = plugin_info.get("icon", "📦")
                name = plugin_info.get("name", plugin_id)
                
                if is_locked:
                    st.markdown(f"{icon} {name} 🔒", help=f"Requires {plugin_info.get('tier_required', 'PRO')} tier")
                else:
                    if st.button(f"{icon} {name}", key=f"nav_{plugin_id}", use_container_width=True):
                        st.session_state.current_page = plugin_id
                        st.rerun()
            
            st.divider()
            
            # Settings
            if st.button("⚙️ " + t.get("settings", "Settings"), key="nav_settings", use_container_width=True):
                st.session_state.current_page = "settings"
                st.rerun()
            
            # Upgrade button for non-PREMIUM users
            if self.license_tier != "PREMIUM":
                st.markdown("---")
                if st.button("⭐ " + t.get("upgrade", "Upgrade"), key="upgrade_button", use_container_width=True, type="primary"):
                    st.session_state.current_page = "upgrade"
                    st.rerun()
    
    def _render_content(self, t):
        """Render main content area"""
        current_page = st.session_state.current_page
        
        if current_page == "dashboard":
            self._render_dashboard(t)
        elif current_page == "settings":
            self._render_settings(t)
        elif current_page == "upgrade":
            self._render_upgrade(t)
        else:
            # Load plugin
            self._render_plugin(current_page, t)
    
    def _render_dashboard(self, t):
        """Render dashboard page"""
        from ui.pages.dashboard import render_dashboard
        render_dashboard(self.config, self.license_tier, t)
    
    def _render_settings(self, t):
        """Render settings page"""
        from ui.pages.settings import render_settings
        render_settings(self.config, self.license_tier, t)
    
    def _render_upgrade(self, t):
        """Render upgrade page"""
        st.markdown("## ⭐ " + t.get("upgrade_title", "Upgrade Your Plan"))
        
        st.markdown(t.get("upgrade_description", "Unlock more features with a paid plan!"))
        
        # Show tier comparison
        tiers = self.config._config.get("tiers", {})
        
        cols = st.columns(len(tiers))
        
        for idx, (tier_name, tier_data) in enumerate(tiers.items()):
            with cols[idx]:
                st.markdown(f"### {tier_name}")
                
                if tier_data.get("price_idr", 0) == 0:
                    st.markdown("**FREE**")
                else:
                    st.markdown(f"**Rp {tier_data['price_idr']:,}** / year")
                
                st.markdown("---")
                
                features = tier_data.get("features", {})
                for feature, enabled in features.items():
                    if enabled:
                        st.markdown(f"✅ {feature.replace('_', ' ').title()}")
                
                if tier_name != self.license_tier and tier_data.get("price_idr", 0) > 0:
                    if st.button(f"Get {tier_name}", key=f"get_{tier_name}"):
                        st.info("🔗 Visit: https://aigem2.com/pricing (Coming soon)")
    
    def _render_plugin(self, plugin_id: str, t):
        """Load and render plugin"""
        
        # Check access
        if not self.plugin_manager.can_access_plugin(plugin_id):
            st.error(f"🔒 This feature requires {self.plugin_manager.get_plugin_tier(plugin_id)} tier or higher.")
            
            if st.button("⭐ Upgrade Now"):
                st.session_state.current_page = "upgrade"
                st.rerun()
            return
        
        # Load plugin
        with st.spinner(f"Loading {plugin_id}..."):
            plugin = self.plugin_manager.load_plugin(plugin_id)
            
            if plugin:
                plugin.render_ui(t)
            else:
                st.error(f"Failed to load plugin: {plugin_id}")
