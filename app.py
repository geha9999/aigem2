"""
AIGEM2 Main Entry Point
"""
import streamlit as st
from config import AppConfig
from ui.pages.dashboard import render_dashboard
from ui.pages.settings import render_settings
from ui.pages.tier_management import render_tier_management

def main():
    config = AppConfig()
    tier = config.get_license_tier()

    st.set_page_config(page_title="AIGEM2", layout="wide")
    if "current_page" not in st.session_state:
        st.session_state.current_page = "dashboard"

    # Sidebar navigation
    with st.sidebar:
        st.markdown("## AIGEM2")
        st.button("🏠 Dashboard", on_click=lambda: st.session_state.update(current_page="dashboard"))
        st.button("⚙️ Settings", on_click=lambda: st.session_state.update(current_page="settings"))
        st.button("💳 Tier Management", on_click=lambda: st.session_state.update(current_page="tier_management"))

    # Main router
    if st.session_state.current_page == "dashboard":
        render_dashboard(tier, config)
    elif st.session_state.current_page == "settings":
        render_settings(config)
    elif st.session_state.current_page == "tier_management":
        render_tier_management(tier, config)
    else:
        st.error("Page not found.")

if __name__ == "__main__":
    main()