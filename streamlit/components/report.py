# import streamlit as st
# from typing import Dict, Any, List


# class ReportDisplay:
#     """Component for displaying detailed SEO reports."""

#     @staticmethod
#     def show_technical_analysis(data: Dict[str, Any]):
#         """Display technical SEO analysis."""
#         st.subheader("Technical SEO Analysis")

#         if not data:
#             st.error("No technical analysis data available.")
#             return

#         # Meta Tags Analysis
#         with st.expander("Meta Tags"):
#             meta_tags = data.get("meta_tags", {})
#             if not meta_tags:
#                 st.write("No meta tags found.")
#             else:
#                 for key, value in meta_tags.items():
#                     st.write(f"**{key.replace('_', ' ').title()}**: {value or 'Not Available'}")

#         # Headings Analysis
#         with st.expander("Headings"):
#             headings = data.get("headings", {})
#             st.write("Heading Counts:")
#             for heading, count in headings.items():
#                 st.write(f"{heading.upper()}: {count}")

#         # Images Analysis
#         with st.expander("Images"):
#             images = data.get("images", {})
#             st.write("Image Statistics:")
#             st.write(f"Total Images: {images.get('total_images', 0)}")
#             st.write(f"Missing Alt Attributes: {images.get('missing_alt', 0)}")
#             st.write(f"Missing Src Attributes: {images.get('missing_src', 0)}")

#         # Links Analysis
#         with st.expander("Links"):
#             links = data.get("links", {})
#             st.write("Link Statistics:")
#             st.write(f"Internal Links: {links.get('internal_links', 0)}")
#             st.write(f"External Links: {links.get('external_links', 0)}")
#             st.write(f"Total Links: {links.get('total_links', 0)}")

#         # Content Quality
#         with st.expander("Content Quality"):
#             content = data.get("content", {})
#             st.write("Content Quality Metrics:")
#             st.write(f"Word Count: {content.get('word_count', 0)}")
#             st.write(f"Paragraphs: {content.get('paragraphs', 0)}")
#             st.write(f"Has Structured Data: {content.get('has_structured_data', False)}")

#         # Technical Elements
#         with st.expander("Technical Elements"):
#             technical = data.get("technical", {})
#             st.write("Technical SEO Elements:")
#             st.write(f"Canonical Tag Present: {technical.get('has_canonical', False)}")
#             st.write(f"Favicon Present: {technical.get('has_favicon', False)}")
#             st.write(f"Viewport Tag Present: {technical.get('has_viewport', False)}")

#     @staticmethod
#     def show_backlink_analysis(data: Dict[str, Any]):
#         """Display backlink analysis."""
#         st.subheader("Backlink Analysis")

#         if not data or "error" in data:
#             st.error("Error retrieving backlink data.")
#             return

#         col1, col2, col3 = st.columns(3)

#         with col1:
#             st.metric("Domain Authority", data.get("domain_authority", 0))
#         with col2:
#             st.metric("Total Links", data.get("total_links", 0))
#         with col3:
#             st.metric("Linking Domains", data.get("linking_domains", 0))

#         # Additional details, if available
#         with st.expander("Backlink Details"):
#             st.json(data)

#     @staticmethod
#     def show_issues_table(issues: List[Dict[str, Any]]):
#         """Display SEO issues and recommendations."""
#         st.subheader("SEO Issues & Recommendations")

#         if not issues:
#             st.write("No issues or recommendations available.")
#             return

#         for issue in issues:
#             with st.expander(f"🔍 {issue['issue']}"):
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     st.write(f"Priority: {issue['priority']}")
#                 with col2:
#                     st.write(f"Estimated Time: {issue['estimated_time']}")

#                 st.write("Steps to Fix:")
#                 for step in issue.get("steps", []):
#                     st.write(f"- {step}")

import streamlit as st
from typing import Dict, Any, List

class ReportDisplay:
    """Component for displaying SEO reports"""
    
    @staticmethod
    def show_overview_metrics(data: Dict[str, Any]):
        st.subheader("SEO-Metrics & Overzicht")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Domein Autoriteit",
                value=data.get('domain_authority', 0)
            )
        
        with col2:
            st.metric(
                label="Page Autoriteit",
                value=data.get('page_authority', 0)
            )
            
        with col3:
            st.metric(
                label="Aantal Backlinks",
                value=data.get('backlinks', 0)
            )

    # @staticmethod
    # def show_technical_analysis(data: Dict[str, Any]):
    #     with st.expander("Technische SEO Analyse", expanded=True):
    #         st.markdown("""
    #         ### Technische SEO Controle
    #         Technische SEO is essentieel om zoekmachines te helpen uw website goed te indexeren en crawlen.
    #         """)
            
    #         # Create technical issues table
    #         if 'technical_issues' in data:
    #             st.table(data['technical_issues'])
    # @staticmethod
    # def show_technical_analysis(data: Dict[str, Any]):
    #     """Display technical SEO analysis"""
    #     # Meta Tags Section
    #     st.subheader("Meta Tags")
    #     meta_data = data.get('meta_tags', {})
        
    #     col1, col2 = st.columns(2)
    #     with col1:
    #         st.metric("Title Length", len(meta_data.get('title', '')) if meta_data.get('title') else 0)
    #     with col2:
    #         st.metric("Description Length", len(meta_data.get('meta_description', '')) if meta_data.get('meta_description') else 0)
        
    #     # Headings Structure
    #     st.subheader("Heading Structure")
    #     headings_data = data.get('headings', {})
    #     heading_cols = st.columns(6)
    #     for i, col in enumerate(heading_cols, 1):
    #         with col:
    #             st.metric(f"H{i}", headings_data.get(f'h{i}', 0))
        
    #     # Technical Elements
    #     st.subheader("Technical Elements")
    #     tech_data = data.get('technical', {})
    #     tech_cols = st.columns(3)
    #     with tech_cols[0]:
    #         st.metric("Canonical", "✓" if tech_data.get('has_canonical') else "✗")
    #     with tech_cols[1]:
    #         st.metric("Viewport", "✓" if tech_data.get('has_viewport') else "✗")
    #     with tech_cols[2]:
    #         st.metric("Favicon", "✓" if tech_data.get('has_favicon') else "✗")
    
    @staticmethod
    def show_technical_analysis(data: Dict[str, Any], enhanced_insights: List[Dict[str, Any]] = None):
        """Display technical SEO analysis with enhanced insights"""
        # Meta Tags Section
        st.subheader("Meta Tags")
        meta_data = data.get('meta_tags', {})
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Title Length", len(meta_data.get('title', '')) if meta_data.get('title') else 0)
        with col2:
            st.metric("Description Length", len(meta_data.get('meta_description', '')) if meta_data.get('meta_description') else 0)
        
        # Headings Structure
        st.subheader("Heading Structure")
        headings_data = data.get('headings', {})
        heading_cols = st.columns(6)
        for i, col in enumerate(heading_cols, 1):
            with col:
                st.metric(f"H{i}", headings_data.get(f'h{i}', 0))
        
        # Technical Elements
        st.subheader("Technical Elements")
        tech_data = data.get('technical', {})
        tech_cols = st.columns(3)
        with tech_cols[0]:
            st.metric("Canonical", "✓" if tech_data.get('has_canonical') else "✗")
        with tech_cols[1]:
            st.metric("Viewport", "✓" if tech_data.get('has_viewport') else "✗")
        with tech_cols[2]:
            st.metric("Favicon", "✓" if tech_data.get('has_favicon') else "✗")

        # Enhanced AI Insights
        if enhanced_insights:
            st.markdown("### AI-Enhanced Technical Insights")
            for insight in enhanced_insights:
                with st.expander(insight.get('title', '')):
                    st.write(insight.get('description', ''))
                    
                    cols = st.columns(4)
                    with cols[0]:
                        st.metric("Priority", insight.get('metadata', {}).get('priority', ''))
                    with cols[1]:
                        st.metric("Impact", f"{float(insight.get('metadata', {}).get('impact', 0))*100:.0f}%")
                    with cols[2]:
                        st.metric("Time", insight.get('metadata', {}).get('implementation_time', ''))
                    with cols[3]:
                        st.metric("Cost", insight.get('metadata', {}).get('estimated_cost', ''))
                    
                    if insight.get('implementation_steps'):
                        st.markdown("#### Implementation Steps")
                        for step in insight['implementation_steps']:
                            st.markdown(f"- {step}")
    
    @staticmethod
    def show_content_analysis(data: Dict[str, Any]):
        with st.expander("Content Analyse", expanded=True):
            # Content metrics
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Woorden", data.get('word_count', 0))
            with col2:
                st.metric("Headers", data.get('total_headings', 0))

    @staticmethod
    def show_backlink_analysis(data: Dict[str, Any]):
        with st.expander("Backlink Analyse", expanded=True):
            st.markdown("### Backlink Profiel")
            
            # Backlink metrics
            if 'backlinks' in data:
                st.table(data['backlinks'])

    @staticmethod
    def show_recommendations(recommendations: List[Dict[str, Any]]):
        with st.expander("SEO Aanbevelingen & Kosten", expanded=True):
            for rec in recommendations:
                st.markdown(f"""
                **{rec['task']}**
                - Prioriteit: {rec['priority']}
                - Tijd: {rec['time']}
                - Kosten: {rec['cost']}
                """)