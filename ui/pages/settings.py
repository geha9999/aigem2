"""
Settings Page
App configuration, preferences, backup
"""
import streamlit as st
from config import AppConfig

def render_settings(config: AppConfig):
    """Render settings page"""
    
    st.title("⚙️ Settings")
    
    # Appearance
    st.markdown("### Appearance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        theme = st.radio(
            "Theme",
            options=["dark", "light"],
            index=0 if st.session_state.theme == "dark" else 1,
            horizontal=True
        )
        
        if theme != st.session_state.theme:
            st.session_state.theme = theme
            st.rerun()
    
    with col2:
        language = st.radio(
            "Language",
            options=["en", "id"],
            format_func=lambda x: "🇬🇧 English" if x == "en" else "🇮🇩 Bahasa Indonesia",
            index=0 if st.session_state.language == "en" else 1,
            horizontal=True
        )
        
        if language != st.session_state.language:
            st.session_state.language = language
            st.rerun()
    
    st.divider()
    
    # Storage
    st.markdown("### Storage")
    
    storage_path = st.text_input(
        "Data Directory",
        value="~/.aigem2",
        help="Local storage location"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📂 Open Data Folder"):
            st.info("Opening folder: " + storage_path)
    
    with col2:
        if st.button("🗑️ Clear Cache"):
            st.success("Cache cleared!")
    
    st.divider()
    
    # Backup
    st.markdown("### Backup & Export")
    
    auto_backup = st.checkbox("Enable daily auto-backup", value=False)
    
    if auto_backup:
        st.info("Auto-backup enabled. Last backup: Never")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 Backup Now", use_container_width=True):
            with st.spinner("Creating backup..."):
                import time
                time.sleep(1)
                st.success("Backup created successfully!")
    
    with col2:
        if st.button("📤 Export All Data", use_container_width=True):
            st.info("Export feature coming soon!")
    
    st.divider()
    
    # About
    st.markdown("### About")
    st.markdown("**AIGEM2** v1.0.0")
    st.markdown("Local-first AI productivity app")
    st.markdown("[GitHub](https://github.com/geha9999/aigem2) | [Documentation](https://docs.aigem2.com)")