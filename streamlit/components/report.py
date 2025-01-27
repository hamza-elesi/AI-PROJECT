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
            meta_tags = data.get("meta_tags", {})
            if not meta_tags:
                st.write("No meta tags found.")
            else:
                for key, value in meta_tags.items():
                    st.write(f"**{key.replace('_', ' ').title()}**: {value or 'Not Available'}")

        # Headings Analysis
        with st.expander("Headings"):
            headings = data.get("headings", {})
            st.write("Heading Counts:")
            for heading, count in headings.items():
                st.write(f"{heading.upper()}: {count}")

        # Images Analysis
        with st.expander("Images"):
            images = data.get("images", {})
            st.write("Image Statistics:")
            st.write(f"Total Images: {images.get('total_images', 0)}")
            st.write(f"Missing Alt Attributes: {images.get('missing_alt', 0)}")
            st.write(f"Missing Src Attributes: {images.get('missing_src', 0)}")

        # Links Analysis
        with st.expander("Links"):
            links = data.get("links", {})
            st.write("Link Statistics:")
            st.write(f"Internal Links: {links.get('internal_links', 0)}")
            st.write(f"External Links: {links.get('external_links', 0)}")
            st.write(f"Total Links: {links.get('total_links', 0)}")

        # Content Quality
        with st.expander("Content Quality"):
            content = data.get("content", {})
            st.write("Content Quality Metrics:")
            st.write(f"Word Count: {content.get('word_count', 0)}")
            st.write(f"Paragraphs: {content.get('paragraphs', 0)}")
            st.write(f"Has Structured Data: {content.get('has_structured_data', False)}")

        # Technical Elements
        with st.expander("Technical Elements"):
            technical = data.get("technical", {})
            st.write("Technical SEO Elements:")
            st.write(f"Canonical Tag Present: {technical.get('has_canonical', False)}")
            st.write(f"Favicon Present: {technical.get('has_favicon', False)}")
            st.write(f"Viewport Tag Present: {technical.get('has_viewport', False)}")

    @staticmethod
    def show_backlink_analysis(data: Dict[str, Any]):
        """Display backlink analysis."""
        st.subheader("Backlink Analysis")

        if not data or "error" in data:
            st.error("Error retrieving backlink data.")
            return

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Domain Authority", data.get("domain_authority", 0))
        with col2:
            st.metric("Total Links", data.get("total_links", 0))
        with col3:
            st.metric("Linking Domains", data.get("linking_domains", 0))

        # Additional details, if available
        with st.expander("Backlink Details"):
            st.json(data)

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
