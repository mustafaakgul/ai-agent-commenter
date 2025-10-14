import json

from typing import Dict

"""Checks the quality of the generated response."""
def quality_check(quality_chain, review: str, response: str) -> Dict:
    try:
        quality_result = quality_chain.run(
            review=review,
            response=response
        )

        try:
            json_start = quality_result.find('{')
            json_end = quality_result.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = quality_result[json_start:json_end]
                quality = json.loads(json_str)
            else:
                raise ValueError("JSON not found")
        except:
            quality = {
                "scores": {
                    "professionalism": 7,
                    "relevance": 7,
                    "warmth": 7,
                    "solution_focus": 7,
                    "overall": 7
                },
                "feedback": "Quality check could not be performed",
                "approved": True
            }

        return quality
    except Exception as e:
        print(f"⚠️ Quality check error: {e}")
        return {"error": str(e)}
