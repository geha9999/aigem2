"""
Dashboard Page
Shows overview, recent activity, quick actions
"""
import streamlit as st
from datetime import datetime

def render_dashboard(config, license_tier, t):
    """Render dashboard page"""   
    st.markdown("## 👋 " + t.get("welcome", "Welcome to AIGEM2!"))
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label=t.get("notes", "Notes"),
            value="0",
            delta="+0 today"
        )
    
    with col2:
        st.metric(
            label=t.get("videos", "Videos"),
            value="0",
            delta="+0 this week"
        )
    
    with col3:
        st.metric(
            label=t.get("storage_used", "Storage Used"),
            value="0 MB",
            delta="/ 100 MB" if license_tier == "FREE" else "/ Unlimited"
        )
    
    with col4:
        st.metric(
            label=t.get("ai_chats", "AI Chats"),
            value="0",
            delta="+0 this month"
        )
    
    st.divider()
    
    # Quick actions
    st.markdown("### ⚡ " + t.get("quick_actions", "Quick Actions"))
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 " + t.get("new_note", "New Note"), use_container_width=True):
            st.session_state.current_page = "knowledge_base"
            st.rerun()
    
    with col2:
        if st.button("🎥 " + t.get("download_video", "Download Video"), use_container_width=True):
            if license_tier in ["STARTER", "PRO", "PREMIUM"]:
                st.session_state.current_page = "video_downloader"
                st.rerun()
            else:
                st.error("🔒 " + t.get("requires_starter", "Requires STARTER tier or higher"))
    
    with col3:
        if st.button("🤖 " + t.get("ai_chat", "AI Chat"), use_container_width=True):
            if license_tier in ["PRO", "PREMIUM"]:
                st.session_state.current_page = "ai_assistant"
                st.rerun()
            else:
                st.error("🔒 " + t.get("requires_pro", "Requires PRO tier or higher"))
    
    st.divider()
    
    # Recent activity
    st.markdown("### 📊 " + t.get("recent_activity", "Recent Activity"))
    
    # Empty state
    st.info("ℹ️ " + t.get("no_activity", "No recent activity. Start by creating a note or downloading a video!"))
    
    st.divider()
    
    # Tips section
    st.markdown("### 💡 " + t.get("tips", "Tips & Tricks"))
    
    tips = [
        "Use `Ctrl+K` to open command palette",
        "Press `Ctrl+N` to quickly create a new note",
        "Toggle dark/light theme with the 🌙/☀️ button",
        "All your data is stored locally and encrypted"
    ]
    
    for tip in tips:
        st.markdown(f"• {tip}")