from typing import Dict, Any, List, Union
import json
from datetime import datetime
from ..rag.processor import RAGProcessor
from ..llm.analyzer import LLMAnalyzer

class AIInsightsGenerator:
    """Generates enhanced SEO insights by combining RAG and LLM outputs."""

    def __init__(self):
        self.rag_processor = RAGProcessor()
        self.llm_analyzer = LLMAnalyzer()

    async def generate_insights(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive insights from RAG & LLM."""
        try:
            print("🟢 Starting AI Insights Generation...")

            # Step 1: Get insights from RAG
            rag_insights = await self.rag_processor.process(data)
            print(f"🔹 RAG Insights Received: {rag_insights}")

            # Step 2: Get insights from LLM
            llm_insights_raw = await self.llm_analyzer.analyze(data)

            # Ensure LLM response is parsed correctly
            llm_insights = self._parse_llm_response(llm_insights_raw)
            print(f"🔹 LLM Insights Parsed: {llm_insights}")

            # Step 3: Combine and enhance insights
            combined_insights = await self._combine_insights(data, rag_insights, llm_insights)

            # Step 4: Ensure priority actions exist
            if not combined_insights.get("priority_actions"):
                combined_insights["priority_actions"] = self._generate_priority_actions(data, rag_insights, llm_insights)

            print(f"✅ Final AI Insights: {combined_insights}")
            return combined_insights

        except Exception as e:
            print(f"❌ AI Insights Generation Error: {e}")
            return {
                'error': str(e),
                'basic_insights': self._generate_basic_insights(data)
            }

    # def _parse_llm_response(self, response: Any) -> Dict[str, Any]:
    #     """Ensure LLM response is correctly formatted."""
    #     try:
    #         if isinstance(response, str):
    #             try:
    #                 parsed_response = json.loads(response)
    #             except json.JSONDecodeError as e:
    #                 print(f"❌ JSON Parsing Error: {e}, returning empty insights.")
    #                 return {}
    #         elif isinstance(response, dict):
    #             parsed_response = response
    #         else:
    #             print("⚠️ LLM response is not a dictionary or valid JSON string.")
    #             return {}

    #         # Transform the response to our expected format
    #         transformed = {
    #             "technical_insights": [],
    #             "content_insights": [],
    #             "strategic_recommendations": []
    #         }
            
    #         # Handle technical insights
    #         if "recommendations" in parsed_response:
    #             recs = parsed_response["recommendations"]
    #             if isinstance(recs, list):
    #                 # Handle list format
    #                 transformed["technical_insights"] = [
    #                     {
    #                         "type": "technical",
    #                         "recommendation": rec,
    #                         "confidence": 0.7
    #                     } for rec in recs
    #                 ]
    #             elif isinstance(recs, dict):
    #                 # Handle dictionary format
    #                 for key, value in recs.items():
    #                     if isinstance(value, dict):
    #                         # Handle nested dictionaries (e.g., meta_tags: {...})
    #                         for subkey, subvalue in value.items():
    #                             transformed["technical_insights"].append({
    #                                 "type": "technical",
    #                                 "metric": subkey,
    #                                 "recommendation": subvalue,
    #                                 "confidence": 0.7
    #                             })
    #                     else:
    #                         transformed["technical_insights"].append({
    #                             "type": "technical",
    #                             "metric": key,
    #                             "recommendation": value,
    #                             "confidence": 0.7
    #                         })
            
    #         # Handle content insights
    #         if "improvements" in parsed_response:
    #             imps = parsed_response["improvements"]
    #             if isinstance(imps, list):
    #                 # Handle list format
    #                 transformed["content_insights"] = [
    #                     {
    #                         "type": "content",
    #                         "recommendation": imp,
    #                         "confidence": 0.7
    #                     } for imp in imps
    #                 ]
    #             elif isinstance(imps, dict):
    #                 # Handle dictionary format
    #                 for category, details in imps.items():
    #                     if isinstance(details, dict):
    #                         for key, value in details.items():
    #                             transformed["content_insights"].append({
    #                                 "type": "content",
    #                                 "metric": key,
    #                                 "recommendation": value,
    #                                 "confidence": 0.7
    #                             })
    #                     else:
    #                         transformed["content_insights"].append({
    #                             "type": category,
    #                             "suggestions": details if isinstance(details, list) else [details],
    #                             "confidence": 0.7
    #                         })
            
    #         # Handle strategic recommendations
    #         if "actionable_steps" in parsed_response:
    #             steps = parsed_response["actionable_steps"]
    #             if isinstance(steps, dict):
    #                 transformed["strategic_recommendations"] = [
    #                     {
    #                         "type": "ai_generated",
    #                         "recommendation": value,
    #                         "confidence": 0.7,
    #                         "source": "llm"
    #                     } for _, value in steps.items()
    #                 ]
    #             elif isinstance(steps, list):
    #                 transformed["strategic_recommendations"] = [
    #                     {
    #                         "type": "ai_generated",
    #                         "recommendation": step,
    #                         "confidence": 0.7,
    #                         "source": "llm"
    #                     } for step in steps
    #                 ]
            
    #         # Validate the transformed data using Pydantic
    #         try:
    #             from src.models.seo_models import AIInsights
    #             validated = AIInsights(**transformed)
    #             return validated.dict()
    #         except Exception as e:
    #             print(f"❌ Pydantic Validation Error: {e}, returning unvalidated data.")
    #             return transformed
                
    #     except Exception as e:
    #         print(f"❌ General Parsing Error: {e}, returning empty insights.")
    #         return {}

    
    # Update the _parse_llm_response method in generator.py
    
    def _parse_llm_response(self, response: Any) -> Dict[str, Any]:
        """Ensure LLM response is correctly formatted."""
        try:
            if isinstance(response, str):
                try:
                    parsed_response = json.loads(response)
                except json.JSONDecodeError as e:
                    print(f"❌ JSON Parsing Error: {e}, returning empty insights.")
                    return {}
            elif isinstance(response, dict):
                parsed_response = response
            else:
                print("⚠️ LLM response is not a dictionary or valid JSON string.")
                return {}

            # Transform the response to our expected format
            transformed = {
                "technical_insights": [],
                "content_insights": [],
                "strategic_recommendations": [],
                "backlink_insights": []
            }
            
            # Process recommendations (technical insights)
            if "recommendations" in parsed_response:
                recs = parsed_response["recommendations"]
                
                # Handle list format (newer format)
                if isinstance(recs, list):
                    for index, rec in enumerate(recs):
                        transformed["technical_insights"].append({
                            "type": "technical",
                            "metric": f"technical_{index}",
                            "recommendation": rec,
                            "priority": "high" if index < 3 else "medium",
                            "impact": 0.8 if index < 3 else 0.6,
                            "confidence": 0.7,
                            "description": f"This recommendation will help improve your technical SEO performance."
                        })
                # Handle dict format (older format)
                elif isinstance(recs, dict):
                    for key, value in recs.items():
                        if isinstance(value, dict):
                            for subkey, subvalue in value.items():
                                transformed["technical_insights"].append({
                                    "type": "technical",
                                    "metric": subkey,
                                    "recommendation": subvalue,
                                    "priority": "high",
                                    "impact": 0.8,
                                    "confidence": 0.7,
                                    "description": f"This recommendation will improve your {key} performance."
                                })
                        else:
                            transformed["technical_insights"].append({
                                "type": "technical",
                                "metric": key,
                                "recommendation": value,
                                "priority": "high",
                                "impact": 0.8,
                                "confidence": 0.7
                            })
            
            # Process improvements (content insights)
            if "improvements" in parsed_response:
                imps = parsed_response["improvements"]
                
                # Handle dict of lists format (newer format)
                if isinstance(imps, dict):
                    for category, details in imps.items():
                        if isinstance(details, list):
                            for index, item in enumerate(details):
                                transformed["content_insights"].append({
                                    "type": "content",
                                    "metric": category,
                                    "recommendation": item,
                                    "priority": "high" if index == 0 else "medium",
                                    "impact": 0.7,
                                    "confidence": 0.7,
                                    "description": f"This improvement will enhance your content {category}."
                                })
                        elif isinstance(details, dict):
                            for key, value in details.items():
                                transformed["content_insights"].append({
                                    "type": "content",
                                    "metric": key,
                                    "recommendation": value,
                                    "priority": "medium",
                                    "impact": 0.7,
                                    "confidence": 0.7
                                })
                        else:
                            transformed["content_insights"].append({
                                "type": "content",
                                "metric": category,
                                "recommendation": str(details),
                                "priority": "medium",
                                "impact": 0.7,
                                "confidence": 0.7
                            })
            
            # Process actionable steps (strategic recommendations)
            if "actionable_steps" in parsed_response:
                steps = parsed_response["actionable_steps"]
                
                if isinstance(steps, dict):
                    for _, value in steps.items():
                        # Check if value is about backlinks
                        if any(keyword in value.lower() for keyword in ["backlink", "link", "authority"]):
                            transformed["backlink_insights"].append({
                                "type": "backlinks",
                                "recommendation": value,
                                "priority": "high",
                                "impact": 0.9,
                                "confidence": 0.7,
                                "description": "This will help improve your backlink profile."
                            })
                        else:
                            transformed["strategic_recommendations"].append({
                                "type": "strategic",
                                "recommendation": value,
                                "priority": "high",
                                "impact": 0.8,
                                "confidence": 0.7,
                                "source": "llm",
                                "description": "This strategic action will improve your overall SEO performance."
                            })
                elif isinstance(steps, list):
                    for step in steps:
                        transformed["strategic_recommendations"].append({
                            "type": "strategic",
                            "recommendation": step,
                            "priority": "high",
                            "impact": 0.8,
                            "confidence": 0.7,
                            "source": "llm"
                        })
            
            # Validate the transformed data using Pydantic
            try:
                from src.models.seo_models import AIInsights
                validated = AIInsights(**transformed)
                return validated.dict()
            except Exception as e:
                print(f"❌ Pydantic Validation Error: {e}, returning unvalidated data.")
                return transformed
                
        except Exception as e:
            print(f"❌ General Parsing Error: {e}, returning empty insights.")
            return {}

    # def _parse_llm_response(self, response: Any) -> Dict[str, Any]:
    #     """Ensure LLM response is correctly formatted using Pydantic validation."""
    #     try:
    #         if isinstance(response, str):
    #             try:
    #                 parsed_response = json.loads(response)
    #             except json.JSONDecodeError as e:
    #                 print(f"❌ JSON Parsing Error: {e}, returning empty insights.")
    #                 return {}
    #         elif isinstance(response, dict):
    #             parsed_response = response
    #         else:
    #             print("⚠️ LLM response is not a dictionary or valid JSON string.")
    #             return {}

    #         # Use Pydantic to validate and transform the LLM response
    #         try:
    #             from src.models.llm_models import LLMResponse
    #             validated_response = LLMResponse(**parsed_response)
    #             return validated_response.dict(exclude_none=True)
    #         except Exception as e:
    #             print(f"❌ LLM Response validation error: {e}")
    #             # If validation fails, return a minimal valid structure
    #             return {
    #                 "technical_insights": [],
    #                 "content_insights": [],
    #                 "backlink_insights": [],
    #                 "strategic_recommendations": []
    #             }
                
    #     except Exception as e:
    #         print(f"❌ General Parsing Error: {e}, returning empty insights.")
    #         return {}
    
    async def _combine_insights(
        self, 
        data: Dict[str, Any],
        rag_insights: Dict[str, Any],
        llm_insights: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Combine and prioritize insights from RAG and LLM."""
        try:
            from src.models.seo_models import AIInsights
            
            combined = {
                'technical_insights': self._merge_insights(
                    rag_insights.get('technical_insights', []),
                    self._convert_to_list(llm_insights.get('technical_insights', []))
                ),
                'content_insights': self._merge_insights(
                    rag_insights.get('content_insights', []),
                    self._convert_to_list(llm_insights.get('content_insights', []))
                ),
                'backlink_insights': self._merge_insights(
                    rag_insights.get('backlink_insights', []),
                    self._convert_to_list(llm_insights.get('backlink_insights', []))
                ),
                'strategic_recommendations': self._merge_strategy_insights(
                    rag_insights.get('similar_cases', []),
                    self._convert_to_list(llm_insights.get('strategic_recommendations', []))
                )
            }
            
            # Generate priority actions
            combined['priority_actions'] = self._generate_priority_actions(data, rag_insights, llm_insights)
            
            # Validate with Pydantic
            insights = AIInsights(**combined)
            
            # Add executive summary
            combined['summary'] = insights.get_executive_summary()
            
            return combined
            
        except Exception as e:
            print(f"❌ Error combining insights: {e}")
            return {
                'error': str(e),
                'basic_insights': self._generate_basic_insights(data)
            }

    # async def _combine_insights(
    #     self, 
    #     data: Dict[str, Any],
    #     rag_insights: Dict[str, Any],
    #     llm_insights: Dict[str, Any]
    # ) -> Dict[str, Any]:
    #     """Combine and prioritize insights from RAG and LLM."""
    #     try:
    #         # Create empty lists if keys are missing
    #         technical_rag = rag_insights.get('technical_insights', [])
    #         technical_llm = self._convert_to_list(llm_insights.get('technical_insights', []))
            
    #         content_rag = rag_insights.get('content_insights', [])
    #         content_llm = self._convert_to_list(llm_insights.get('content_insights', []))
            
    #         backlink_rag = rag_insights.get('backlink_insights', [])
    #         backlink_llm = self._convert_to_list(llm_insights.get('backlink_insights', []))
            
    #         strategic_rag = rag_insights.get('similar_cases', [])
    #         strategic_llm = self._convert_to_list(llm_insights.get('strategic_recommendations', []))
            
    #         combined = {
    #             'technical_insights': self._merge_insights(technical_rag, technical_llm),
    #             'content_insights': self._merge_insights(content_rag, content_llm),
    #             'backlink_insights': self._merge_insights(backlink_rag, backlink_llm),
    #             'strategic_recommendations': self._merge_strategy_insights(strategic_rag, strategic_llm)
    #         }
            
    #         # Generate priority actions
    #         combined['priority_actions'] = self._generate_priority_actions(data, rag_insights, llm_insights)
            
    #         # Validate with Pydantic and add executive summary
    #         try:
    #             from src.models.seo_models import AIInsights
    #             insights = AIInsights(**combined)
    #             combined['summary'] = insights.get_executive_summary()
    #             return combined
    #         except Exception as e:
    #             print(f"❌ AIInsights validation error: {e}, continuing without validation")
    #             # Add basic summary without validation
    #             combined['summary'] = {
    #                 "total_insights": (
    #                     len(combined.get('technical_insights', [])) + 
    #                     len(combined.get('content_insights', [])) + 
    #                     len(combined.get('backlink_insights', []))
    #                 ),
    #                 "critical_issues": len([
    #                     a for a in combined.get('priority_actions', []) 
    #                     if isinstance(a, dict) and a.get('priority', '').lower() == "high"
    #                 ]),
    #                 "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #             }
    #             return combined
            
    #     except Exception as e:
    #         print(f"❌ Error combining insights: {e}")
    #         return {
    #             'error': str(e),
    #             'basic_insights': self._generate_basic_insights(data)
    #         }

    def _convert_to_list(self, data: Any) -> List:
        """Ensure insights are always in list format to prevent type errors."""
        if data is None:
            return []
            
        if isinstance(data, dict):
            # If it's a dictionary of lists
            if all(isinstance(v, list) for v in data.values()):
                return sum(data.values(), [])
            # If it's a dictionary of values
            result = []
            for key, value in data.items():
                if isinstance(value, dict):
                    # Handle nested dictionaries
                    for subkey, subvalue in value.items():
                        result.append({
                            "metric": subkey,
                            "recommendation": subvalue
                        })
                else:
                    result.append({
                        "metric": key,
                        "recommendation": value
                    })
            return result
        elif isinstance(data, list):
            # If it's already a list
            return [
                item if isinstance(item, dict) else {"recommendation": item}
                for item in data
            ]
        elif isinstance(data, str):
            # If it's a single string
            return [{"recommendation": data}]
        return []

    def _merge_insights(self, rag_insights: List, llm_insights: List) -> List[Dict]:
        """Merge and deduplicate insights."""
        merged = []
        seen_recommendations = set()
        
        # Process all insights
        for insight in rag_insights + llm_insights:
            if not insight:
                continue
                
            try:
                # Normalize the insight
                normalized = {}
                
                if isinstance(insight, dict):
                    # If it's a dictionary
                    rec = insight.get('recommendation', '')
                    if isinstance(rec, dict):
                        # Handle nested recommendation dictionary
                        rec_text = ' '.join(str(v) for v in rec.values())
                    elif isinstance(rec, list):
                        # Handle list of recommendations
                        rec_text = ' '.join(str(r) for r in rec)
                    else:
                        # Handle string recommendation
                        rec_text = str(rec)
                    
                    # Create a unique key
                    key = f"{insight.get('metric', '')}_{rec_text[:50]}"
                    
                    # Copy the insight
                    normalized = insight.copy()
                    
                elif isinstance(insight, str):
                    # If it's a string
                    key = insight[:50]
                    normalized = {
                        "recommendation": insight,
                        "confidence": 0.7
                    }
                else:
                    # Skip if it's an unsupported type
                    continue
                    
                # Add if not seen
                if key not in seen_recommendations:
                    # Ensure confidence is set
                    if 'confidence' not in normalized:
                        normalized['confidence'] = self._calculate_confidence(normalized)
                        
                    merged.append(normalized)
                    seen_recommendations.add(key)
                    
            except Exception as e:
                print(f"❌ Error merging insight: {e}")
                continue
                
        # Sort by confidence
        return sorted(merged, key=lambda x: x.get('confidence', 0), reverse=True)

    # def _merge_insights(self, rag_insights: List, llm_insights: List) -> List[Dict]:
    #     """Merge and deduplicate insights."""
    #     merged = []
    #     seen_recommendations = set()
        
    #     # Process all insights
    #     for insight in rag_insights + llm_insights:
    #         if not insight:
    #             continue
                
    #         try:
    #             # Normalize the insight
    #             normalized = {}
                
    #             if isinstance(insight, dict):
    #                 # If it's a dictionary
    #                 rec = insight.get('recommendation', '')
    #                 if isinstance(rec, dict):
    #                     # Handle nested recommendation dictionary
    #                     rec_text = ' '.join(str(v) for v in rec.values())
    #                 elif isinstance(rec, list):
    #                     # Handle list of recommendations
    #                     rec_text = ' '.join(str(r) for r in rec)
    #                 else:
    #                     # Handle string recommendation
    #                     rec_text = str(rec)
                    
    #                 # Create a unique key
    #                 key = f"{insight.get('metric', '')}_{rec_text[:50]}"
                    
    #                 # Copy the insight
    #                 normalized = insight.copy()
                    
    #                 # Ensure confidence is set to a numeric value
    #                 if 'confidence' not in normalized or normalized['confidence'] is None:
    #                     normalized['confidence'] = self._calculate_confidence(normalized)
                    
    #             elif isinstance(insight, str):
    #                 # If it's a string
    #                 key = insight[:50]
    #                 normalized = {
    #                     "recommendation": insight,
    #                     "confidence": 0.7
    #                 }
    #             else:
    #                 # Skip if it's an unsupported type
    #                 continue
                    
    #             # Add if not seen
    #             if key not in seen_recommendations:
    #                 merged.append(normalized)
    #                 seen_recommendations.add(key)
                    
    #         except Exception as e:
    #             print(f"❌ Error merging insight: {e}")
    #             continue
                
    #     # Sort by confidence
    #     return sorted(merged, key=lambda x: x.get('confidence', 0), reverse=True)

    # def _calculate_confidence(self, insight: Dict[str, Any]) -> float:
    #     """Calculate confidence score for an insight."""
    #     base_confidence = insight.get('confidence', 0.5)
    #     impact = insight.get('impact', 0.5)
    #     evidence = 1 if insight.get('evidence') else 0.6
        
    #     return (base_confidence + impact + evidence) / 3    
    
    # def _calculate_confidence(self, insight: Dict[str, Any]) -> float:
    #     """Calculate confidence score for an insight."""
    #     base_confidence = insight.get('confidence', 0.5)
    #     if base_confidence is None:
    #         base_confidence = 0.5
            
    #     impact = insight.get('impact', 0.5)
    #     if impact is None:
    #         impact = 0.5
            
    #     evidence = 1 if insight.get('evidence') else 0.6
        
    #     return (base_confidence + impact + evidence) / 3

    def _calculate_confidence(self, insights: List[Dict[str, Any]]) -> float:
        """Safely calculate score with default values"""
        try:
            impact = float(insights.get('impact', 0.5))
            confidence = float(insights.get('confidence', 0.5))
            return impact 
        except (TypeError, ValueError) as e:
            print(f"Warning: Error calculating score: {e}")
            return 0.5  # Safe default

    def _merge_strategy_insights(self, similar_cases: List[Dict], llm_recommendations: List[Dict]) -> List[Dict]:
        """Generate strategic insights based on similar cases and LLM recommendations."""
        strategic_insights = []

        for case in similar_cases:
            if isinstance(case, dict) and case.get('similarity_score', 0) > 0.5:
                strategic_insights.append({
                    'type': 'case_based',
                    'recommendation': case.get('content'),
                    'confidence': case.get('similarity_score'),
                    'source': 'similar_case'
                })

        for rec in llm_recommendations:
            if isinstance(rec, dict):
                strategic_insights.append({
                    'type': 'ai_generated',
                    'recommendation': rec.get('recommendation', 'No Recommendation'),
                    'confidence': 0.7,
                    'source': 'llm'
                })

        return sorted(strategic_insights, key=lambda x: x['confidence'], reverse=True)

    def _get_priority_insights(self, insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract priority insights from a set of insights."""
        priority_insights = []

        for category in ['technical_insights', 'content_insights', 'backlink_insights']:
            for insight in insights.get(category, []):
                if insight.get('impact', 0) > 0.7:
                    priority_insights.append(insight)

        return priority_insights

    # def _generate_priority_actions(self, data: Dict[str, Any], rag_insights: Dict[str, Any], llm_insights: Dict[str, Any]) -> List[Dict[str, Any]]:
    #     """Generate prioritized action items."""
    #     all_insights = self._get_priority_insights(rag_insights) + self._get_priority_insights(llm_insights)

    #     if not all_insights:
    #         return self._generate_basic_priority_actions(data)

    #     return sorted(all_insights, key=lambda x: (x.get('impact', 0) * x.get('confidence', 0)), reverse=True)[:5]

    def _generate_priority_actions(self, data: Dict[str, Any], rag_insights: Dict[str, Any], llm_insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate prioritized action items."""
        all_insights = self._get_priority_insights(rag_insights) + self._get_priority_insights(llm_insights)

        if not all_insights:
            return self._generate_basic_priority_actions(data)

        # Filter out insights with None confidence or impact
        valid_insights = [
            insight for insight in all_insights
            if insight.get('impact') is not None and insight.get('confidence') is not None
        ]

        # Sort valid insights by priority score
        sorted_insights = sorted(
            valid_insights,
            key=lambda x: (x.get('impact', 0) * x.get('confidence', 0)),
            reverse=True
        )[:5]

        # If no valid insights, fall back to basic insights
        if not sorted_insights:
            return self._generate_basic_priority_actions(data)

        return sorted_insights

    def _generate_basic_priority_actions(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate basic priority actions without AI processing."""
        return sorted(
            self._basic_technical_insights(data) +
            self._basic_content_insights(data) +
            self._basic_backlink_insights(data),
            key=lambda x: x.get('impact', 0),
            reverse=True
        )[:3]
    
    def _generate_basic_insights(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback basic insights when AI fails."""
        return {
            'technical_insights': self._basic_technical_insights(data),
            'content_insights': self._basic_content_insights(data),
            'backlink_insights': self._basic_backlink_insights(data),
            'priority_actions': self._generate_basic_priority_actions(data)
        }
    
    def _basic_technical_insights(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fallback technical SEO insights."""
        return [{'type': 'technical', 'metric': 'meta_description', 'recommendation': 'Add a relevant meta description for better SEO.', 'priority': 'high', 'impact': 0.8}]

    def _basic_content_insights(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fallback content SEO insights."""
        return [{'type': 'content', 'metric': 'word_count', 'recommendation': 'Increase content length to at least 300 words.', 'priority': 'high', 'impact': 0.7}]

    def _basic_backlink_insights(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fallback backlink insights."""
        return [{'type': 'backlinks', 'metric': 'total_links', 'recommendation': 'Increase backlinks to improve authority.', 'priority': 'high', 'impact': 0.9}]
