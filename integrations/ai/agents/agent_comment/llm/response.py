import json

from typing import Dict

"""Generates a response for the review using Claude."""
def generate_response(response_chain, review_data: Dict, analysis: Dict) -> str:
    try:
        response = response_chain.run(
            customer_name=review_data['customer'],
            product_name=review_data['product'],
            review=review_data['review'],
            analysis=json.dumps(analysis, ensure_ascii=False, indent=2)
        )
        return response.strip()
    except Exception as e:
        print(f"❌ Response generation error: {e}")
        return """Değerli müşterimiz,

        Yorumunuz için teşekkür ederiz. Şu anda sistemimizde geçici bir sorun yaşanmaktadır.
        Lütfen daha sonra tekrar deneyin veya müşteri hizmetlerimizle iletişime geçin.

        Saygılarımızla,
        Müşteri Hizmetleri"""
