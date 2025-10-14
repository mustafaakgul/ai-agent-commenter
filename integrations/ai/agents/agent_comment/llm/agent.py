import os

from typing import List, Dict
from dotenv import load_dotenv
from datetime import datetime

from langchain_anthropic import ChatAnthropic
from langchain.memory import ConversationBufferMemory
from .chains import setup_chains
from .utils import load_reviews_from_text
from .analysis import analyze_review
from .response import generate_response
from .quality import quality_check
from .persistence import save_results

load_dotenv()

# Main agent class and orchestration
class ECommerceReviewAgent:
    def __init__(self, anthropic_api_key: str = None, model_name: str = "claude-3-sonnet-20240229"):
        """Initializes the Claude agent for e-commerce review responses."""
        self.llm = ChatAnthropic(
            model=model_name,
            anthropic_api_key=anthropic_api_key or os.getenv("ANTHROPIC_API_KEY"),
            temperature=0.7,
            max_tokens=1000
        )
        self.memory = ConversationBufferMemory(return_messages=True)
        self.analysis_chain, self.response_chain, self.quality_chain = setup_chains(self.llm)

    """Processes all reviews and generates responses."""
    def process_all_reviews(self, content: str, enable_quality_check: bool = True) -> List[Dict]:
        reviews = load_reviews_from_text(content)
        results = []

        for i, review_data in enumerate(reviews, 1):
            analysis = analyze_review(self.analysis_chain, review_data['review'])

            if 'error' not in analysis:
                response = generate_response(self.response_chain, review_data, analysis)
                quality = {}

                if enable_quality_check:
                    quality = quality_check(self.quality_chain, review_data['review'], response)

                result = {
                    'original': review_data,
                    'analysis': analysis,
                    'generated_response': response,
                    'quality_check': quality,
                    'processed_at': datetime.now().isoformat()
                }
            else:
                result = {
                    'original': review_data,
                    'analysis': analysis,
                    'generated_response': "Response could not be generated due to analysis error.",
                    'quality_check': {},
                    'processed_at': datetime.now().isoformat()
                }
            results.append(result)
        return results

    def save_results(self, id: int, results: List[Dict]):
        save_results(id, results)
