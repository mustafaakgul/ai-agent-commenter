import re

from datetime import datetime
from typing import List, Dict

"""Utility functions for review parsing and rating extraction"""

def load_reviews_from_text(content: str) -> List[Dict]:
    reviews = []

    try:
        blocks = content.split('\n\n')
        review_id = 1

        for block in blocks:
            lines = [line.strip() for line in block.split('\n') if line.strip()]

            if len(lines) == 0:
                continue

            # Format 1: "Product|Customer|Review"
            if '|' in lines[0] and lines[0].count('|') >= 2:
                parts = lines[0].split('|')
                reviews.append({
                    'id': review_id,
                    'product': parts[0].strip(),
                    'customer': parts[1].strip(),
                    'review': parts[2].strip(),
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'rating': extract_rating('|'.join(parts[3:]) if len(parts) > 3 else "")
                })
            # Format 2: Multi-line format
            elif len(lines) >= 3:
                product = lines[0].replace('Ürün:', '').strip()
                customer = lines[1].replace('Müşteri:', '').strip()
                review = '\n'.join(lines[2:]).replace('Yorum:', '').strip()

                reviews.append({
                    'id': review_id,
                    'product': product,
                    'customer': customer,
                    'review': review,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'rating': extract_rating(review)
                })
            # Format 3: Only review
            else:
                reviews.append({
                    'id': review_id,
                    'product': 'Not specified',
                    'customer': 'Anonymous Customer',
                    'review': ' '.join(lines),
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'rating': extract_rating(' '.join(lines))
                })

            review_id += 1
    except Exception as e:
        print(f"Error: {e}")
    return reviews

def extract_rating(text: str) -> int:
    """Attempts to extract star rating from text."""
    rating_patterns = [
        r'(\d+)\s*yıldız',
        r'(\d+)\s*/\s*5',
        r'(\d+)\s*/\s*10',
        r'⭐' * 5,
    ]

    for pattern in rating_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1))

    star_count = text.count('⭐')
    if star_count > 0:
        return min(star_count, 5)
    return 0
