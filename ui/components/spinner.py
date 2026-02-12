"""
Loading Spinner Component
"""
import streamlit as st

def render_spinner(message: str = "Loading..."):
    """Render loading spinner with message"""
    return st.spinner(message)