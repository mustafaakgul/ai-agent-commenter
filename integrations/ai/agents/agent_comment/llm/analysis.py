import json

from typing import Dict

"""Analyzes the review using Claude."""
def analyze_review(analysis_chain, review: str) -> Dict:
    try:
        analysis_result = analysis_chain.run(review=review)

        try:
            json_start = analysis_result.find('{')
            json_end = analysis_result.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = analysis_result[json_start:json_end]
                analysis = json.loads(json_str)
            else:
                raise ValueError("JSON not found")
        except (json.JSONDecodeError, ValueError) as e:
            print(f"⚠️ JSON parse error, using default analysis: {e}")
            analysis = {
                "sentiment": "neutral",
                "sentiment_score": 5,
                "category": "general",
                "urgency": "medium",
                "keywords": ["customer", "review"],
                "summary": review[:100] + "..." if len(review) > 100 else review,
                "main_issues": ["could not analyze"],
                "requires_action": True,
                "response_tone": "friendly"
            }
        return analysis
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return {"error": str(e)}
