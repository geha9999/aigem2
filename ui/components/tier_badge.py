"""
Tier Badge Component
Displays user's current tier with styled badge
"""
import streamlit as st

def render_tier_badge(tier: str):
    """Render tier badge"""
    
    badge_styles = {
        "FREE": {
            "bg": "#334155",
            "color": "#94A3B8",
            "icon": "🆓"
        },
        "STARTER": {
            "bg": "rgba(59, 130, 246, 0.1)",
            "color": "#60A5FA",
            "icon": "⭐"
        },
        "PRO": {
            "bg": "rgba(16, 185, 129, 0.1)",
            "color": "#34D399",
            "icon": "💎"
        },
        "PREMIUM": {
            "bg": "linear-gradient(135deg, #F59E0B 0%, #D97706 100%)",
            "color": "white",
            "icon": "👑"
        }
    }
    
    style = badge_styles.get(tier, badge_styles["FREE"])
    
    badge_html = f"""
    <div style="
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        border-radius: 6px;
        background: {style['bg']};
        color: {style['color']};
        font-weight: 500;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    ">
        {style['icon']} {tier}
    </div>
    """
    
    st.markdown(badge_html, unsafe_allow_html=True)