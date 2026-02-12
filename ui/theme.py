"""
Theme Manager
Switch between dark and light themes
"""
import streamlit as st

def apply_theme(theme: str = "dark"):
    """Apply theme CSS"""    
    if theme == "dark":
        css = """
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
            --warning: #FBBF24;
            --danger: #F87171;
            --border: #334155;
        }
        
        .stApp {
            background-color: var(--bg-primary);
            color: var(--text-primary);
        }
        
        .stButton>button {
            background-color: var(--primary);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        .stButton>button:hover {
            background-color: var(--primary-hover);
            transform: translateY(-1px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.4);
        }
        
        .stTextInput>div>div>input {
            background-color: var(--bg-secondary);
            color: var(--text-primary);
            border: 1px solid var(--border);
            border-radius: 8px;
        }
        
        .stTextInput>div>div>input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.1);
        }
        
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: var(--text-primary);
        }
        
        .stMarkdown p {
            color: var(--text-secondary);
        }
        
        .stSidebar {
            background-color: var(--bg-secondary);
        }
        
        .stSidebar .stButton>button {
            background-color: transparent;
            color: var(--text-secondary);
            border: 1px solid transparent;
            justify-content: flex-start;
            text-align: left;
        }
        
        .stSidebar .stButton>button:hover {
            background-color: var(--bg-tertiary);
            color: var(--text-primary);
            transform: none;
        }
        
        hr {
            border-color: var(--border);
        }
        </style>
        """
    else:  # light theme
        css = """
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
            --warning: #F59E0B;
            --danger: #EF4444;
            --border: #E5E7EB;
        }
        
        .stApp {
            background-color: var(--bg-primary);
            color: var(--text-primary);
        }
        
        .stButton>button {
            background-color: var(--primary);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        .stButton>button:hover {
            background-color: var(--primary-hover);
            transform: translateY(-1px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        }
        
        .stTextInput>div>div>input {
            background-color: var(--bg-secondary);
            color: var(--text-primary);
            border: 1px solid var(--border);
            border-radius: 8px;
        }
        
        .stTextInput>div>div>input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: var(--text-primary);
        }
        
        .stMarkdown p {
            color: var(--text-secondary);
        }
        
        .stSidebar {
            background-color: var(--bg-secondary);
            border-right: 1px solid var(--border);
        }
        
        .stSidebar .stButton>button {
            background-color: transparent;
            color: var(--text-secondary);
            border: 1px solid transparent;
            justify-content: flex-start;
            text-align: left;
        }
        
        .stSidebar .stButton>button:hover {
            background-color: var(--bg-tertiary);
            color: var(--text-primary);
            transform: none;
        }
        
        hr {
            border-color: var(--border);
        }
        </style>
        """
    
    st.markdown(css, unsafe_allow_html=True)

def toggle_theme(current_theme: str) -> str:
    """Toggle between dark and light theme"""
    return "light" if current_theme == "dark" else "dark"