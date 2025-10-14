import os

from dotenv import load_dotenv
from .agent import ECommerceReviewAgent

load_dotenv()

def execute(id, content):
    API_KEY = os.getenv("ANTHROPIC_API_KEY")

    try:
        # Run Agent
        agent = ECommerceReviewAgent(
            anthropic_api_key=API_KEY,
            model_name="claude-3-5-sonnet-20241022"
        )

        # Process Comments
        results = agent.process_all_reviews(
            content=content,
            enable_quality_check=True  # Enable Quality Check
        )

        # Save Results
        agent.save_results(id, results)
    except Exception as e:
        print(f"Error: {e}")
