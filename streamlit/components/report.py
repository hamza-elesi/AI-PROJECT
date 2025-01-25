import streamlit as st
from typing import Dict, Any

class ReportDisplay:
    """Component for displaying SEO reports"""
    
    @staticmethod
    def show_issues_table(issues: List[Dict[str, Any]]):
        """Display issues and recommendations"""
        st.subheader("Problemen & Aanbevelingen")
        
        for issue in issues:
            with st.expander(f"🔍 {issue['issue']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write("Prioriteit:", issue['priority'])
                with col2:
                    st.write("Geschatte Tijd:", issue['estimated_time'])
                with col3:
                    st.write("Geschatte Kosten:", issue['estimated_cost'])
                
                st.write("Stappen:")
                for step in issue['steps']:
                    st.write(f"- {step}")

    @staticmethod
    def show_technical_analysis(data: Dict[str, Any]):
        """Display technical SEO analysis"""
        st.subheader("Technische SEO Analyse")
        
        with st.expander("Meta Tags"):
            st.json(data.get('meta_tags', {}))
            
        with st.expander("Technische Elements"):
            st.json(data.get('technical_elements', {}))