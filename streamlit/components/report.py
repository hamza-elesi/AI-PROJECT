import streamlit as st
from typing import Dict, Any, List


class ReportDisplay:
    """Component for displaying detailed SEO reports."""

    @staticmethod
    def show_technical_analysis(data: Dict[str, Any]):
        """Display technical SEO analysis."""
        st.subheader("Technical SEO Analysis")

        if not data:
            st.error("No technical analysis data available.")
            return

        # Meta Tags Analysis
        with st.expander("Meta Tags"):
            st.json(data.get("meta_tags", {}))

        # Technical Elements Analysis
        with st.expander("Technical Elements"):
            st.json(data.get("technical_elements", {}))

    @staticmethod
    def show_backlink_analysis(backlinks_data: Dict[str, Any]):
        """Display backlink analysis."""
        st.subheader("Backlink Analysis")

        if not backlinks_data or "error" in backlinks_data:
            st.error("Error retrieving backlink data.")
            return

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Domain Authority", backlinks_data.get("domain_authority", "N/A"))
        with col2:
            st.metric("Total Links", backlinks_data.get("total_links", "N/A"))
        with col3:
            st.metric("Linking Domains", backlinks_data.get("linking_domains", "N/A"))

    @staticmethod
    def show_issues_table(issues: List[Dict[str, Any]]):
        """Display SEO issues and recommendations."""
        st.subheader("SEO Issues & Recommendations")

        if not issues:
            st.write("No issues or recommendations available.")
            return

        for issue in issues:
            with st.expander(f"🔍 {issue['issue']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"Priority: {issue['priority']}")
                with col2:
                    st.write(f"Estimated Time: {issue['estimated_time']}")

                st.write("Steps to Fix:")
                for step in issue.get("steps", []):
                    st.write(f"- {step}")
