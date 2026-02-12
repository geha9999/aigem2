"""
Settings Page
Manage app preferences, account, storage
"""
import streamlit as st
from pathlib import Path

def render_settings(config, license_tier, t):
    """Render settings page"""    
    st.markdown("## ⚙️ " + t.get("settings", "Settings"))
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎨 " + t.get("appearance", "Appearance"),
        "💾 " + t.get("storage", "Storage"),
        "💳 " + t.get("tier_billing", "Tier & Billing"),
        "ℹ️ " + t.get("about", "About")
    ])
    
    with tab1:
        render_appearance_settings(t)
    
    with tab2:
        render_storage_settings(license_tier, t)
    
    with tab3:
        render_tier_settings(config, license_tier, t)
    
    with tab4:
        render_about_settings(t)

def render_appearance_settings(t):
    """Render appearance settings"""    
    st.markdown("### " + t.get("theme", "Theme"))
    
    theme_mode = st.radio(
        t.get("choose_theme", "Choose theme"),
        options=["dark", "light"],
        format_func=lambda x: "🌙 Dark" if x == "dark" else "☀️ Light",
        horizontal=True,
        key="theme_radio"
    )
    
    if theme_mode != st.session_state.theme_mode:
        st.session_state.theme_mode = theme_mode
        st.rerun()
    
    st.divider()
    
    st.markdown("### " + t.get("language", "Language"))
    
    language = st.radio(
        t.get("choose_language", "Choose language"),
        options=["en", "id"],
        format_func=lambda x: "🇬🇧 English" if x == "en" else "🇮🇩 Bahasa Indonesia",
        horizontal=True,
        key="language_radio"
    )
    
    if language != st.session_state.language:
        st.session_state.language = language
        st.rerun()

def render_storage_settings(license_tier, t):
    """Render storage settings"""    
    st.markdown("### " + t.get("storage_usage", "Storage Usage"))
    
    # Mock data (would come from database)
    storage_data = {
        "notes": 0,
        "videos": 0,
        "recordings": 0,
        "total": 0
    }
    
    # Get storage limit
    if license_tier == "FREE":
        limit_mb = 100
    elif license_tier == "STARTER":
        limit_mb = 2000
    else:
        limit_mb = -1  # Unlimited
    
    # Display usage
    if limit_mb == -1:
        st.info(f"📦 Total: {storage_data['total']} MB / ♾️ Unlimited")
    else:
        progress = storage_data['total'] / limit_mb if limit_mb > 0 else 0
        st.progress(progress)
        st.info(f"📦 Total: {storage_data['total']} MB / {limit_mb} MB")
    
    # Breakdown
    st.markdown("**Breakdown:**")
    st.markdown(f"• Notes: {storage_data['notes']} MB")
    st.markdown(f"• Videos: {storage_data['videos']} MB")
    st.markdown(f"• Recordings: {storage_data['recordings']} MB")
    
    st.divider()
    
    st.markdown("### " + t.get("backup", "Backup & Export"))
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 " + t.get("export_all", "Export All Data"), use_container_width=True):
            st.info("Feature coming soon!")
    
    with col2:
        if st.button("🔄 " + t.get("restore", "Restore from Backup"), use_container_width=True):
            st.info("Feature coming soon!")

def render_tier_settings(config, license_tier, t):
    """Render tier and billing settings"""    
    st.markdown("### " + t.get("current_tier", "Current Tier"))
    
    from ui.components.tier_badge import render_tier_badge
    render_tier_badge(license_tier, size="lg")
    
    st.markdown("")
    
    # Tier info
    tier_config = config.get_tier_config(license_tier)
    
    if license_tier == "FREE":
        st.markdown("**Features:**")
        st.markdown("• Basic notes and folders")
        st.markdown("• Text search")
        st.markdown("• 100MB storage")
        st.markdown("• 3 video downloads/month")
        
        st.divider()
        
        if st.button("⭐ " + t.get("upgrade", "Upgrade to Paid Tier"), type="primary", use_container_width=True):
            st.session_state.current_page = "upgrade"
            st.rerun()
    
    else:
        price_idr = tier_config.get("price_idr", 0)
        price_usd = tier_config.get("price_usd", 0)
        
        st.markdown(f"**Price:** Rp {price_idr:,} / ${price_usd}")
        
        st.markdown("**Features:**")
        features = tier_config.get("features", {})
        for feature, enabled in features.items():
            if enabled:
                st.markdown(f"✅ {feature.replace('_', ' ').title()}")
        
        st.divider()
        
        st.markdown("### " + t.get("license_key", "License Key"))
        st.text_input(
            t.get("your_license_key", "Your license key"),
            value="XXXX-XXXX-XXXX-XXXX-XXXX",
            disabled=True,
            type="password"
        )
        
        if st.button("📋 " + t.get("copy_key", "Copy License Key")):
            st.success("✅ " + t.get("copied", "Copied to clipboard!"))

def render_about_settings(t):
    """Render about section"""    
    st.markdown("### " + t.get("about_aigem2", "About AIGEM2"))
    
    st.markdown("""
    **AIGEM2** is a local-first AI-powered productivity application.
    
    **Version:** 1.0.0  
    **Developer:** geha9999  
    **Website:** https://aigem2.com (Coming soon)
    
    ---
    
    **Privacy-First Philosophy:**
    - ✅ All data stored locally on your device
    - ✅ AES-256 encryption
    - ✅ No telemetry by default
    - ✅ Export your data anytime
    
    ---
    
    **Open Source Libraries:**
    - Streamlit (UI framework)
    - yt-dlp (Video downloader)
    - OpenAI Whisper (Transcription)
    - LangChain (AI orchestration)
    - Ollama (Local LLM runtime)
    
    Thank you to all contributors! ❤️
    """)
    st.divider()
    
    if st.button("📄 " + t.get("view_license", "View License"), use_container_width=True):
        st.info("GNU GPL v3.0")
    
    if st.button("🐛 " + t.get("report_bug", "Report Bug"), use_container_width=True):
        st.info("Visit: https://github.com/geha9999/aigem2/issues")