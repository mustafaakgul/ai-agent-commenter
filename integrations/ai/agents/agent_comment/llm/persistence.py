from datetime import datetime
from typing import List, Dict
from app.comments.models import Comment, CommentAnalyzer, CommentQualityScore

# Persistence function for saving results to the database
def save_results(id: int, results: List[Dict]):
    try:
        comment = Comment.objects.get(id=id)
        result = results[0]
        original = result['original']
        analysis = result['analysis']
        response = result['generated_response']
        quality = result.get('quality_check', {})

        # Update Comment Model
        comment.response = response
        comment.status = "WAITING_FOR_APPROVE"
        comment.save()

        # Customer original['customer']
        # Product original['product']
        # Rating original.get('rating', 'N/A')
        # Date original['date']
        # Comment original['review']
        # Emotion/Sentiment analysis['sentiment'] (analysis['sentiment_score']/10)

        # Create CommentAnalyzer
        analyzer = CommentAnalyzer(
            comment=comment,
            analyzed_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            sentiment=analysis.get('sentiment', 'N/A'),
            sentiment_score=analysis.get('sentiment_score', 'N/A'),
            category=analysis.get('category', 'N/A'),
            urgency=analysis.get('urgency', 'N/A'),
            keywords=','.join(analysis.get('keywords', [])),
            summary=analysis.get('summary', ''),
            main_issue=','.join(analysis.get('main_issues', [])),
            required_action=analysis.get('requires_action', False),
            response_tone=analysis.get('tone', 'professional'),
            response=response,
            quality_control=str(quality.get('scores', {})) if quality else ''
        )
        analyzer.save()
        if quality and 'scores' in quality:
            scores = quality['scores']
            CommentQualityScore.objects.create(
                comment=comment,
                professionalism=scores.get('professionalism', 0),
                relevance=scores.get('relevance', 0),
                warmth=scores.get('warmth', 0),
                solution_focus=scores.get('solution_focus', 0),
                overall=scores.get('overall', 0),
                feedback=quality.get('feedback', ''),
                approved=quality.get('approved', False)
            )
    except Exception as e:
        print(f"❌ Error while saving results: {e}")
