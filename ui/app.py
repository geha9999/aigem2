"""
Main Streamlit App with Lazy Module Loading
"""
import streamlit as st
from pathlib import Path

class MainApp:
    """Main application with modular architecture"""
    
    def __init__(self, config, license_status):
        self.config = config
        self.tier = license_status
        self.modules_loaded = {}
    
    def run(self):
        """Run main application"""
        # Apply custom CSS
        self._apply_theme()
        
        # Sidebar navigation
        self._render_sidebar()
        
        # Main content area
        self._render_main_content()
    
    def _apply_theme(self):
        """Apply custom theme (Dark/Light)"""
        # Get theme from session state (default: dark)
        theme = st.session_state.get('theme', 'dark')
        
        # Load theme CSS
        css_file = Path(__file__).parent / 'styles' / f'{theme}_theme.css'
        
        if css_file.exists():
            st.markdown(f'<style>{{css_file.read_text()}}</style>', unsafe_allow_html=True)
    
    def _render_sidebar(self):
        """Render sidebar navigation"""
        with st.sidebar:
            st.title("🎯 AIGEM2")
            
            # Theme toggle
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🌙" if st.session_state.get('theme') == 'light' else "☀️"):
                    st.session_state.theme = 'light' if st.session_state.get('theme') == 'dark' else 'dark'
                    st.rerun()
            
            with col2:
                lang = st.selectbox("🌍", ["EN", "ID"], label_visibility="collapsed")
                st.session_state.language = lang
            
            st.divider()
            
            # Navigation menu
            menu_items = self._get_menu_items()
            
            for item in menu_items:
                icon = item['icon']
                label = item['label']
                module_id = item['module_id']
                tier_required = item.get('tier_required', 'FREE')
                
                # Check if user has access
                if self._has_access(tier_required):
                    if st.button(f"{icon} {label}", key=module_id, use_container_width=True):
                        st.session_state.current_module = module_id
                else:
                    st.button(
                        f"🔒 {label}", 
                        key=module_id, 
                        disabled=True,
                        use_container_width=True,
                        help=f"Requires {tier_required} tier"
                    )
            
            st.divider()
            
            # Tier badge
            self._render_tier_badge()
    
    def _get_menu_items(self):
        """Get navigation menu items"""
        return [
            {"icon": "🏠", "label": "Dashboard", "module_id": "dashboard", "tier_required": "FREE"},
            {"icon": "📚", "label": "Knowledge Base", "module_id": "knowledge_base", "tier_required": "FREE"},
            {"icon": "🎥", "label": "Video Downloader", "module_id": "video_downloader", "tier_required": "STARTER"},
            {"icon": "🎙️", "label": "Transcription", "module_id": "transcription", "tier_required": "STARTER"},
            {"icon": "🖥️", "label": "Screen Recorder", "module_id": "screen_recorder", "tier_required": "PRO"},
            {"icon": "🤖", "label": "AI Assistant", "module_id": "ai_assistant", "tier_required": "PRO"},
            {"icon": "📋", "label": "Meeting Notes", "module_id": "meeting_notes", "tier_required": "PRO"},
            {"icon": "🔄", "label": "Content Tools", "module_id": "content_tools", "tier_required": "PREMIUM"},
            {"icon": "🔌", "label": "Plugins", "module_id": "plugins", "tier_required": "FREE"},
            {"icon": "⚙️", "label": "Settings", "module_id": "settings", "tier_required": "FREE"},
        ]
    
    def _has_access(self, tier_required: str) -> bool:
        """Check if user tier has access to feature"""
        tier_levels = {"FREE": 0, "STARTER": 1, "PRO": 2, "PREMIUM": 3}
        user_level = tier_levels.get(self.tier, 0)
        required_level = tier_levels.get(tier_required, 0)
        return user_level >= required_level
    
    def _render_tier_badge(self):
        """Render current tier badge"""
        tier_colors = {
            "FREE": "#6B7280",
            "STARTER": "#3B82F6",
            "PRO": "#10B981",
            "PREMIUM": "#F59E0B"
        }
        
        color = tier_colors.get(self.tier, "#6B7280")
        
        st.markdown(f"""
        <div style=\"
            background: {color};
            color: white;
            padding: 8px;
            border-radius: 8px;
            text-align: center;
            font-weight: 600;
            margin-top: 16px;
        ">
            {self.tier} TIER
        </div>
        """, unsafe_allow_html=True)
        
        if self.tier != "PREMIUM":
            if st.button("✨ Upgrade", use_container_width=True):
                st.session_state.current_module = "upgrade"
    
    def _render_main_content(self):
        """Render main content area (lazy load modules)"""
        current_module = st.session_state.get('current_module', 'dashboard')
        
        # Show loading spinner
        with st.spinner(f'Loading {current_module}...'):
            self._load_module(current_module)
    
    def _load_module(self, module_id: str):
        """Lazy load module on demand"""
        # Check if already loaded
        if module_id in self.modules_loaded:
            module = self.modules_loaded[module_id]
            module.render()
            return
        
        # Load module dynamically
        try:
            if module_id == "dashboard":
                from ui.pages.dashboard import DashboardPage
                module = DashboardPage(self.config, self.tier)
            
            elif module_id == "knowledge_base":
                from modules.knowledge_base.main import KnowledgeBaseModule
                module = KnowledgeBaseModule(self.config, self.tier)
            
            elif module_id == "video_downloader":
                if not self._has_access("STARTER"):
                    self._show_upgrade_prompt("STARTER")
                    return
                from modules.video_downloader.main import VideoDownloaderModule
                module = VideoDownloaderModule(self.config, self.tier)
            
            elif module_id == "settings":
                from ui.pages.settings import SettingsPage
                module = SettingsPage(self.config, self.tier)
            
            else:
                st.warning(f"Module '{module_id}' not yet implemented")
                return
            
            # Cache module
            self.modules_loaded[module_id] = module
            
            # Render
            module.render()
            
        except Exception as e:
            st.error(f"Error loading module: {e}")
    
    def _show_upgrade_prompt(self, tier_required: str):
        """Show upgrade prompt for locked features"""
        tier_config = self.config.get_tier_config(tier_required)
        price_idr = tier_config.get('price_idr', 0)
        
        st.warning(f"🔒 This feature requires **{tier_required}** tier")
        
        st.info(f"""
        **Upgrade to {tier_required}**
        
        Price: Rp {price_idr:,}/year
        
        Features unlocked:
        - Unlimited video downloads
        - Full transcription
        - Subtitle generator
        - And more!
        """)
        
        if st.button("🚀 Upgrade Now", type="primary"):
            st.session_state.current_module = "upgrade"
            st.rerun()\n    
    def _load_module(self, module_id: str):
        """Lazy load module on demand"""
        # Check if already loaded
        if module_id in self.modules_loaded:
            module = self.modules_loaded[module_id]
            module.render()
            return
        
        # Load module dynamically
        try:
            if module_id == "dashboard":
                from ui.pages.dashboard import DashboardPage
                module = DashboardPage(self.config, self.tier)
            
            elif module_id == "knowledge_base":
                from modules.knowledge_base.main import KnowledgeBaseModule
                module = KnowledgeBaseModule(self.config, self.tier)
            
            elif module_id == "video_downloader":
                if not self._has_access("STARTER"):
                    self._show_upgrade_prompt("STARTER")
                    return
                from modules.video_downloader.main import VideoDownloaderModule
                module = VideoDownloaderModule(self.config, self.tier)
            
            elif module_id == "settings":
                from ui.pages.settings import SettingsPage
                module = SettingsPage(self.config, self.tier)
            
            else:
                st.warning(f"Module '{module_id}' not yet implemented")
                return
            
            # Cache module
            self.modules_loaded[module_id] = module
            
            # Render
            module.render()
            
        except Exception as e:
            st.error(f"Error loading module: {e}")
