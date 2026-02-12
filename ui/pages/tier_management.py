"""
Tier Management Page
License activation, upgrade, quota monitoring
"""
import streamlit as st
from config import AppConfig

def render_tier_management(tier: str, config: AppConfig):
    """Render tier management page"""
    
    st.title("💳 Tier Management")
    
    # Current tier status
    st.markdown("### Current Tier")
    
    from ui.components.tier_badge import render_tier_badge
    render_tier_badge(tier)
    
    tier_config = config.get_tier_config(tier)
    
    if tier == "FREE":
        st.info("You're currently on the FREE tier with limited features.")
    else:
        st.success(f"You're on the {tier} tier. Thank you for your support! 🙏")
    
    st.divider()
    
    # Tier comparison
    st.markdown("### Available Tiers")
    
    tiers = config._config.get("tiers", {})
    
    cols = st.columns(len(tiers))
    
    for idx, (tier_name, tier_data) in enumerate(tiers.items()):
        with cols[idx]:
            st.markdown(f"#### {tier_name}")
            
            price_idr = tier_data.get("price_idr", 0)
            if price_idr == 0:
                st.markdown("**FREE**")
            else:
                billing = tier_data.get("billing_period", "yearly")
                st.markdown(f"**Rp {price_idr:,}**/{billing}")
            
            st.markdown("---")
            
            # Features
            features = tier_data.get("features", {})
            for feature, enabled in features.items():
                if enabled:
                    feature_label = feature.replace("_", " ").title()
                    st.markdown(f"✅ {feature_label}")
            
            # Storage
            storage = tier_data.get("storage_limit_mb", 0)
            if storage == -1:
                st.markdown("✅ Unlimited Storage")
            else:
                st.markdown(f"📦 {storage}MB Storage")
            
            # CTA
            if tier_name != tier:
                if tier_name == "FREE":
                    st.button("Current Tier", disabled=True, use_container_width=True)
                else:
                    if st.button(f"Upgrade to {tier_name}", key=f"upgrade_{tier_name}", use_container_width=True):
                        st.session_state.show_activation = tier_name
                        st.rerun()
            else:
                st.button("✅ Active", disabled=True, use_container_width=True)
    
    st.divider()
    
    # License activation
    if hasattr(st.session_state, 'show_activation'):
        st.markdown("### Activate License")
        
        st.info(f"To activate {st.session_state.show_activation} tier, please enter your license key.")
        
        license_key = st.text_input(
            "License Key",
            placeholder="XXXX-XXXX-XXXX-XXXX-XXXX",
            help="License key from your purchase email"
        )
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if st.button("Activate", type="primary"):
                if license_key:
                    with st.spinner("Activating license..."):
                        import time
                        time.sleep(2)
                        st.success("License activated successfully!")
                        st.balloons()
                else:
                    st.error("Please enter a license key")
        
        with col2:
            if st.button("Cancel"):
                del st.session_state.show_activation
                st.rerun()
    else:
        st.markdown("### Need a License?")
        st.markdown("Purchase a license to unlock premium features:")
        st.markdown("- 🌐 Visit: [aigem2.com/pricing](#)")
        st.markdown("- 📧 Email: sales@aigem2.com")