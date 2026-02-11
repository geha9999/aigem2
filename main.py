"""
AIGEM2 - Local-First AI-Powered Productivity Application
Main launcher with fast startup and lazy module loading
"""
import streamlit as st
import sys
import os
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

# Configure Streamlit page (MUST be first Streamlit command)
st.set_page_config(
    page_title="AIGEM2",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import core modules
from config import AppConfig
from ui.app import MainApp
from licensing.client.license_validator import check_license_validity

def main():
    """Main entry point - lightweight and fast"""
    
    # Initialize config
    config = AppConfig()
    
    # Check license status
    license_status = check_license_validity()
    
    # Initialize main app
    app = MainApp(config, license_status)
    app.run()

if __name__ == "__main__":
    main()
