"""
Dashboard Page
Shows overview, recent activity, quick actions
"""
import streamlit as st
from config import AppConfig

def render_dashboard(tier: str, config: AppConfig):
    """Render dashboard page"""
    
    st.title("🏠 Dashboard")
    
    # Welcome message
    st.markdown(f"### Welcome to AIGEM2!")
    st.markdown(f"Current tier: **{tier}**")
    
    st.divider()
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Notes", "0", help="Notes in Knowledge Base")
    
    with col2:
        st.metric("Videos Downloaded", "0", help="Total videos downloaded")
    
    with col3:
        st.metric("Storage Used", "0 MB", help="Local storage usage")
    
    st.divider()
    
    # Quick actions
    st.markdown("### Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 New Note", use_container_width=True):
            st.session_state.current_page = "knowledge_base"
            st.rerun()
    
    with col2:
        if tier != "FREE":
            if st.button("🎥 Download Video", use_container_width=True):
                st.session_state.current_page = "video_downloader"
                st.rerun()
        else:
            st.button("🎥 Download Video (STARTER+)", use_container_width=True, disabled=True)
    
    with col3:
        if tier in ["PRO", "PREMIUM"]:
            if st.button("🤖 AI Assistant", use_container_width=True):
                st.session_state.current_page = "ai_assistant"
                st.rerun()
        else:
            st.button("🤖 AI Assistant (PRO+)", use_container_width=True, disabled=True)
    
    st.divider()
    
    # Tier comparison
    if tier == "FREE":
        st.info("💡 Upgrade to unlock more features!")
        
        tier_config = config.get_tier_config("STARTER")
        
        st.markdown("**STARTER Tier Benefits:**")
        st.markdown(f"- Unlimited video downloads")
        st.markdown(f"- Transcription & subtitles")
        st.markdown(f"- 2GB storage")
        st.markdown(f"- Only **Rp {tier_config.get('price_idr', 99000):,}**/year")
        
        if st.button("⬆️ Upgrade Now"):
            st.session_state.current_page = "tier_management"
            st.rerun()
