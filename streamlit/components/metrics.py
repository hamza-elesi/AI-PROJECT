import streamlit as st
from typing import Dict, Any


class MetricsDisplay:
    """Component for displaying overview metrics."""

    @staticmethod
    def show_overview(overview: Dict[str, Any]):
        """Display general SEO metrics overview."""
        st.subheader("Overview Metrics")

        if not overview:
            st.error("No overview data available.")
            return

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Domain Authority", overview.get("domain_authority", 0))
        with col2:
            st.metric("Page Authority", overview.get("page_authority", 0))
        with col3:
            st.metric("Total Links", overview.get("total_links", 0))

        with st.expander("Meta Tags"):
            st.json(overview.get("meta_tags", {}))
