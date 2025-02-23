from pydantic import BaseModel, Field, validator, root_validator
from typing import List, Dict, Union, Optional, Any
from datetime import datetime


# RAG Models
class RAGInsight(BaseModel):
    type: str
    metric: Optional[str] = None
    recommendation: str
    priority: str
    impact: float
    confidence: Optional[float] = None
    description: Optional[str] = None

class RAGSimilarCase(BaseModel):
    content: str
    category: str
    similarity_score: float
    rank: int

class RAGResponse(BaseModel):
    technical_insights: List[RAGInsight] = []
    content_insights: List[RAGInsight] = []
    backlink_insights: List[RAGInsight] = []
    similar_cases: List[RAGSimilarCase] = []
    
@root_validator(pre=True)
def ensure_valid_insights(cls, values):
    """Ensure all insights are properly formatted"""
    for field in ['technical_insights', 'content_insights', 'backlink_insights']:
        if field in values and values[field]:
            insights = []
            for insight in values[field]:
                if isinstance(insight, dict):
                    # Ensure required fields
                    if 'recommendation' not in insight:
                        insight['recommendation'] = "No recommendation provided"
                    if 'type' not in insight:
                        insight['type'] = field.split('_')[0]
                    if 'priority' not in insight:
                        insight['priority'] = "medium"
                    if 'impact' not in insight:
                        insight['impact'] = 0.5
                    # Set default confidence if missing or None
                    if 'confidence' not in insight or insight['confidence'] is None:
                        insight['confidence'] = 0.5
                    insights.append(insight)
            values[field] = insights
    return values
    
# Technical SEO Models
class TechnicalInsight(BaseModel):
    type: str = "technical"
    metric: Optional[str] = None
    recommendation: Union[str, Dict[str, str]]
    priority: str = "medium"
    impact: float = 0.5
    confidence: Optional[float] = None
    description: Optional[str] = None
    
    @validator('recommendation')
    def validate_recommendation(cls, v):
        """Convert string recommendations to a standard format"""
        if isinstance(v, str):
            return {"text": v}
        return v

# Content SEO Models
class ContentInsight(BaseModel):
    type: str = "content"
    metric: Optional[str] = None
    recommendation: Union[str, Dict[str, str]]
    priority: str = "medium"
    impact: float = 0.5
    confidence: Optional[float] = None
    description: Optional[str] = None
    suggestions: Optional[List[str]] = None

# Backlink Models
class BacklinkInsight(BaseModel):
    type: str = "backlinks"
    metric: Optional[str] = None
    recommendation: Union[str, Dict[str, str]]
    priority: str = "medium"
    impact: float = 0.5
    confidence: Optional[float] = None
    description: Optional[str] = None

# Strategic Recommendation
class StrategicRecommendation(BaseModel):
    type: str = "strategic"
    recommendation: str
    confidence: float = 0.7
    source: str = "llm"
    description: Optional[str] = None

# Priority Action
class PriorityAction(BaseModel):
    type: str
    metric: Optional[str] = None
    recommendation: str
    priority: str = "high"
    impact: float
    implementation_time: Optional[str] = None
    estimated_cost: Optional[str] = None
    description: Optional[str] = None

# Complete Insights Response
class AIInsights(BaseModel):
    technical_insights: List[TechnicalInsight] = []
    content_insights: List[ContentInsight] = []
    backlink_insights: List[BacklinkInsight] = []
    strategic_recommendations: List[StrategicRecommendation] = []
    priority_actions: List[PriorityAction] = []
    summary: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None
    
    def get_executive_summary(self) -> Dict[str, Any]:
        """Generate an executive summary from the insights"""
        if self.summary:
            return self.summary
            
        return {
            "total_insights": (
                len(self.technical_insights) + 
                len(self.content_insights) + 
                len(self.backlink_insights)
            ),
            "critical_issues": len([
                a for a in self.priority_actions 
                if a.priority.lower() == "high"
            ]),
            "technical_score": self._calculate_score(self.technical_insights),
            "content_score": self._calculate_score(self.content_insights),
            "backlink_score": self._calculate_score(self.backlink_insights),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def _calculate_score(self, insights: List[Any]) -> int:
        """Calculate a score based on impact and confidence"""
        if not insights:
            return 0
            
        total = 0
        count = 0
        
        for insight in insights:
            impact = 0.5
            confidence = 0.5
            
            if isinstance(insight, dict):
                impact = insight.get('impact', 0.5)
                # Set default confidence if None
                confidence = insight.get('confidence')
                if confidence is None:
                    confidence = 0.5
            else:
                impact = getattr(insight, 'impact', 0.5)
                # Set default confidence if None
                confidence = getattr(insight, 'confidence', None)
                if confidence is None:
                    confidence = 0.5
            
            total += impact * confidence
            count += 1
            
        return int((total / count) * 100) if count > 0 else 0