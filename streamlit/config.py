import streamlit as st

class Config:
    """Configuration settings for Streamlit app"""
    
    TITLE = "SEO Analyse Tool"
    
    # Page settings
    PAGE_ICON = "📊"
    LAYOUT = "wide"
    
    # API Settings
    API_TIMEOUT = 30
    
    @staticmethod
    def setup_page():
        """Configure initial page settings"""
        st.set_page_config(
            page_title=Config.TITLE,
            page_icon=Config.PAGE_ICON,
            layout=Config.LAYOUT
        )