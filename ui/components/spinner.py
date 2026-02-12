"""
Custom Loading Spinner Component
"""
import streamlit as st
from contextlib import contextmanager

@contextmanager
def loading_spinner(message: str = "Loading..."):
    """Context manager for loading spinner with custom styling"""    
    spinner_html = f"""
    <div style="display: flex; flex-direction: column; align-items: center; padding: 2rem;">
        <div style="
            border: 3px solid #334155;
            border-top-color: #60A5FA;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
        "></div>
        <p style="margin-top: 1rem; color: #CBD5E1; font-size: 14px;">{message}</p>
    </div>
    
    <style>
    @keyframes spin {{
        to {{ transform: rotate(360deg); }}
    }}
    </style>
    """    
    placeholder = st.empty()
    placeholder.markdown(spinner_html, unsafe_allow_html=True)
    
    try:
        yield
    finally:
        placeholder.empty()