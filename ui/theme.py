"""
Theme Manager
Handles dark/light theme switching
"""
import streamlit as st

class ThemeManager:
    """Manage application themes"""
    
    DARK_THEME = """
    <style>
    :root {
        --bg-primary: #0F172A;
        --bg-secondary: #1E293B;
        --bg-tertiary: #334155;
        --text-primary: #F1F5F9;
        --text-secondary: #CBD5E1;
        --text-tertiary: #94A3B8;
        --primary: #60A5FA;
        --primary-hover: #3B82F6;
        --success: #34D399;
        --danger: #F87171;
        --warning: #FBBF24;
        --border: #334155;
    }
    
    .stApp {
        background-color: var(--bg-primary);
        color: var(--text-primary);
    }
    
    .stButton>button {
        background-color: var(--primary);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        background-color: var(--primary-hover);
        transform: translateY(-1px);
    }
    
    .stTextInput>div>div>input {
        background-color: var(--bg-secondary);
        color: var(--text-primary);
        border: 1px solid var(--border);
        border-radius: 8px;
    }
    
    .stSelectbox>div>div>select {
        background-color: var(--bg-secondary);
        color: var(--text-primary);
        border: 1px solid var(--border);
        border-radius: 8px;
    }
    
    [data-testid="stSidebar"] {
        background-color: var(--bg-secondary);
        border-right: 1px solid var(--border);
    }
    
    hr {
        border-color: var(--border);
    }
    </style>
    """
    
    LIGHT_THEME = """
    <style>
    :root {
        --bg-primary: #F8F9FA;
        --bg-secondary: #FFFFFF;
        --bg-tertiary: #F1F3F5;
        --text-primary: #1F2937;
        --text-secondary: #6B7280;
        --text-tertiary: #9CA3AF;
        --primary: #3B82F6;
        --primary-hover: #2563EB;
        --success: #10B981;
        --danger: #EF4444;
        --warning: #F59E0B;
        --border: #E5E7EB;
    }
    
    .stApp {
        background-color: var(--bg-primary);
        color: var(--text-primary);
    }
    
    .stButton>button {
        background-color: var(--primary);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        background-color: var(--primary-hover);
        transform: translateY(-1px);
    }
    
    .stTextInput>div>div>input {
        background-color: var(--bg-secondary);
        color: var(--text-primary);
        border: 1px solid var(--border);
        border-radius: 8px;
    }
    
    .stSelectbox>div>div>select {
        background-color: var(--bg-secondary);
        color: var(--text-primary);
        border: 1px solid var(--border);
        border-radius: 8px;
    }
    
    [data-testid="stSidebar"] {
        background-color: var(--bg-secondary);
        border-right: 1px solid var(--border);
    }
    
    hr {
        border-color: var(--border);
    }
    </style>
    """
    
    def apply(self, mode: str = "dark"):
        """Apply theme to app""" 
        if mode == "dark":
            st.markdown(self.DARK_THEME, unsafe_allow_html=True)
        else:
            st.markdown(self.LIGHT_THEME, unsafe_allow_html=True)