# streamlit/components/ai_insights.py

import streamlit as st
from typing import Dict, Any

class AIInsightsDisplay:
    """Component for displaying AI-enhanced SEO insights"""
    
    @staticmethod
    def show_enhanced_insights(insights: Dict[str, Any]):
        """Display enhanced AI insights"""
        st.header("AI-Enhanced Insights")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        summary = insights.get('summary', {})
        
        with col1:
            st.metric(
                "Total Insights",
                summary.get('total_insights', 0)
            )
        with col2:
            st.metric(
                "Critical Issues",
                summary.get('critical_issues', 0)
            )
        with col3:
            st.metric(
                "Quick Wins",
                summary.get('quick_wins', 0)
            )
        with col4:
            st.metric(
                "Estimated Cost",
                summary.get('estimated_total_cost', '$0')
            )

    @staticmethod
    def show_strategic_insights(insights: Dict[str, Any]):
        """Display strategic insights"""
        st.subheader("Strategic Recommendations")
        
        strategic = insights.get('strategic', [])
        for insight in strategic:
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"### {insight.get('title', '')}")
                    st.write(insight.get('description', ''))
                
                with col2:
                    st.metric(
                        "Impact Score",
                        f"{insight.get('metadata', {}).get('impact', 0)*100:.0f}%"
                    )
                
                # Impact details
                st.markdown("#### Impact Analysis")
                impact_col1, impact_col2, impact_col3 = st.columns(3)
                
                with impact_col1:
                    st.markdown("**Long Term Impact**")
                    st.write(insight.get('long_term_impact', ''))
                
                with impact_col2:
                    st.markdown("**Competitive Advantage**")
                    st.write(insight.get('competitive_advantage', ''))
                
                with impact_col3:
                    st.markdown("**Resource Requirements**")
                    st.write(insight.get('resource_requirements', ''))

    @staticmethod
    def show_priority_actions(insights: Dict[str, Any]):
        """Display priority actions"""
        st.subheader("Priority Actions")
        
        priorities = insights.get('priorities', [])
        for i, action in enumerate(priorities, 1):
            with st.expander(f"{i}. {action.get('title', '')}"):
                st.write(action.get('description', ''))
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Priority", action.get('metadata', {}).get('priority', ''))
                with col2:
                    st.metric("Time", action.get('metadata', {}).get('implementation_time', ''))
                with col3:
                    st.metric("Cost", action.get('metadata', {}).get('estimated_cost', ''))
                
                if action.get('implementation_steps'):
                    st.markdown("#### Implementation Steps")
                    for step in action['implementation_steps']:
                        st.markdown(f"- {step}")

    @staticmethod
    def show_confidence_metrics(insights: Dict[str, Any]):
        """Display AI confidence metrics"""
        metadata = insights.get('metadata', {})
        
        st.subheader("Analysis Confidence")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                "Confidence Score",
                f"{metadata.get('confidence_score', 0)*100:.0f}%"
            )
        with col2:
            st.metric(
                "Completeness Score",
                f"{metadata.get('completeness_score', 0)*100:.0f}%"
            )