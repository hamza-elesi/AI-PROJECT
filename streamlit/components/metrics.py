import streamlit as st
from typing import Dict, Any

class MetricsDisplay:
    """Component for displaying SEO metrics"""
    
    @staticmethod
    def show_overview(data: Dict[str, Any]):
        """Display overview metrics"""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="SEO Score",
                value=f"{data.get('seo_score', 0)}/100"
            )
            
        with col2:
            st.metric(
                label="Domain Autoriteit",
                value=data.get('domain_authority', 0)
            )
            
        with col3:
            st.metric(
                label="Backlinks",
                value=data.get('total_backlinks', 0)
            )

    @staticmethod
    def show_search_console_metrics(data: Dict[str, Any]):
        """Display Google Search Console metrics"""
        st.subheader("Search Console Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Clicks", data.get('clicks', 0))
        with col2:
            st.metric("Impressies", data.get('impressions', 0))
        with col3:
            st.metric("CTR", f"{data.get('ctr', 0)}%")
        with col4:
            st.metric("Gem. Positie", round(data.get('position', 0), 1))