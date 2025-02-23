from pydantic import BaseModel, Field, root_validator, validator
from typing import List, Dict, Union, Optional, Any
from datetime import datetime

# Models for the different response formats
class TechnicalRecommendation(BaseModel):
    type: str = "technical"
    metric: Optional[str] = None
    recommendation: str
    priority: str = "high"
    impact: float = 0.8
    confidence: float = 0.7
    description: Optional[str] = None

class ContentImprovement(BaseModel):
    type: str = "content"
    metric: Optional[str] = None
    recommendation: str
    priority: str = "medium"
    impact: float = 0.7
    confidence: float = 0.7
    description: Optional[str] = None

class StrategicAction(BaseModel):
    type: str = "strategic"
    recommendation: str
    priority: str = "high"
    impact: float = 0.8
    confidence: float = 0.7
    source: str = "llm"
    description: Optional[str] = None

# Main response models for each type of LLM output format
class RecommendationsResponse(BaseModel):
    recommendations: Union[List[str], Dict[str, Union[str, Dict[str, str]]]]
    
    @validator('recommendations')
    def validate_recommendations(cls, v):
        """Convert various recommendation formats to a standard list format"""
        result = []
        if isinstance(v, dict):
            # Handle nested dict format
            for category, items in v.items():
                if isinstance(items, dict):
                    # Format like {"meta_tags": {"description": "Add a meta description"}}
                    for key, value in items.items():
                        result.append(TechnicalRecommendation(
                            metric=key,
                            recommendation=value,
                            description=f"Improve your {category} by updating the {key}."
                        ))
                else:
                    # Format like {"key": "value"}
                    result.append(TechnicalRecommendation(
                        metric=category,
                        recommendation=items,
                        description=f"Improve your {category}."
                    ))
        elif isinstance(v, list):
            # Format like ["recommendation1", "recommendation2"]
            for i, item in enumerate(v):
                result.append(TechnicalRecommendation(
                    metric=f"technical_{i}",
                    recommendation=item,
                    description="This technical improvement will enhance your SEO performance."
                ))
        return result

class ImprovementsResponse(BaseModel):
    improvements: Union[Dict[str, Union[List[Dict[str, str]], Dict[str, str], List[str]]], List[Dict[str, str]]]
    
    @validator('improvements')
    def validate_improvements(cls, v):
        """Convert various improvement formats to a standard list format"""
        result = []
        if isinstance(v, dict):
            for category, items in v.items():
                if isinstance(items, list):
                    # Format like {"category": [{"recommendation": "text", "priority": "high"}]}
                    if all(isinstance(item, dict) for item in items):
                        for item in items:
                            result.append(ContentImprovement(
                                metric=category,
                                recommendation=item.get('recommendation', ''),
                                priority=item.get('priority', 'medium').lower(),
                                description=f"This will improve your content {category}."
                            ))
                    # Format like {"category": ["text1", "text2"]}
                    else:
                        for item in items:
                            result.append(ContentImprovement(
                                metric=category,
                                recommendation=item,
                                description=f"This will improve your content {category}."
                            ))
                elif isinstance(items, dict):
                    # Format like {"category": {"key": "value"}}
                    for key, value in items.items():
                        result.append(ContentImprovement(
                            metric=key,
                            recommendation=value,
                            description=f"This will improve your {category} by addressing {key}."
                        ))
                else:
                    # Format like {"category": "text"}
                    result.append(ContentImprovement(
                        metric=category,
                        recommendation=items,
                        description=f"This will improve your {category}."
                    ))
        elif isinstance(v, list):
            # Format like [{"recommendation": "text", "priority": "high"}]
            for item in v:
                if isinstance(item, dict):
                    result.append(ContentImprovement(
                        recommendation=item.get('recommendation', ''),
                        priority=item.get('priority', 'medium').lower(),
                        description=item.get('description', 'This will improve your content quality.')
                    ))
        return result

class ActionableStepsResponse(BaseModel):
    actionable_steps: Union[Dict[str, str], List[str]]
    
    @validator('actionable_steps')
    def validate_steps(cls, v):
        """Convert various step formats to a standard list format"""
        result = []
        if isinstance(v, dict):
            # Format like {"1": "Step one text", "2": "Step two text"}
            for key, value in v.items():
                result.append(StrategicAction(
                    recommendation=value,
                    description=f"Strategic action {key} will improve your SEO performance."
                ))
        elif isinstance(v, list):
            # Format like ["Step one text", "Step two text"]
            for item in v:
                result.append(StrategicAction(
                    recommendation=item,
                    description="This strategic action will improve your SEO performance."
                ))
        return result

# Combined model that can process any of the response formats
class LLMResponse(BaseModel):
    technical_insights: List[TechnicalRecommendation] = []
    content_insights: List[ContentImprovement] = []
    backlink_insights: List[StrategicAction] = []
    strategic_recommendations: List[StrategicAction] = []
    
    @root_validator(pre=True)
    def process_response(cls, values):
        """Process various response formats into standardized structures"""
        processed = {
            "technical_insights": [],
            "content_insights": [],
            "backlink_insights": [],
            "strategic_recommendations": []
        }
        
        # Process recommendations
        if 'recommendations' in values:
            try:
                model = RecommendationsResponse(recommendations=values['recommendations'])
                processed['technical_insights'] = model.recommendations
            except Exception as e:
                print(f"⚠️ Error processing recommendations: {e}")
        
        # Process improvements
        if 'improvements' in values:
            try:
                model = ImprovementsResponse(improvements=values['improvements'])
                processed['content_insights'] = model.improvements
            except Exception as e:
                print(f"⚠️ Error processing improvements: {e}")
        
        # Process actionable steps
        if 'actionable_steps' in values:
            try:
                model = ActionableStepsResponse(actionable_steps=values['actionable_steps'])
                # Categorize actionable steps between backlinks and general strategic recommendations
                for step in model.actionable_steps:
                    rec = step.recommendation.lower()
                    if "backlink" in rec or "link" in rec or "authority" in rec:
                        processed['backlink_insights'].append(step)
                    else:
                        processed['strategic_recommendations'].append(step)
            except Exception as e:
                print(f"⚠️ Error processing actionable steps: {e}")
        
        return processed