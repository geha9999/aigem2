"""Tier Badge Component
Displays user's current tier with styling"""import streamlit as st

def render_tier_badge(tier: str, size: str = "md"):
    """Render tier badge"""    
    tier_styles = {
        "FREE": {
            "bg": "#6B728020",
            "border": "#6B7280",
            "color": "#6B7280"
        },
        "STARTER": {
            "bg": "#3B82F620",
            "border": "#3B82F6",
            "color": "#3B82F6"
        },
        "PRO": {
            "bg": "#10B98120",
            "border": "#10B981",
            "color": "#10B981"
        },
        "PREMIUM": {
            "bg": "linear-gradient(135deg, #F59E0B 0%, #D97706 100%)",
            "border": "#F59E0B",
            "color": "#FFFFFF"
        }
    }
    
    sizes = {
        "sm": {"padding": "2px 8px", "font-size": "11px"},
        "md": {"padding": "4px 12px", "font-size": "12px"},
        "lg": {"padding": "6px 16px", "font-size": "14px"}
    }
    
    style = tier_styles.get(tier, tier_styles["FREE"])
    size_style = sizes.get(size, sizes["md"])
    
    # Special handling for PREMIUM gradient
    if tier == "PREMIUM":
        bg_style = f"background: {style['bg']};"
    else:
        bg_style = f"background: {style['bg']};"
    
    badge_html = f"""
    <div style="
        {bg_style}
        border: 1px solid {style['border']};
        border-radius: 6px;
        padding: {size_style['padding']};
        display: inline-flex;
        align-items: center;
        font-size: {size_style['font-size']};
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: {style['color']};
        {' box-shadow: 0 2px 4px rgba(245, 158, 11, 0.3);' if tier == 'PREMIUM' else ''}
    ">
        {tier}
    </div>
    """    
    st.markdown(badge_html, unsafe_allow_html=True)