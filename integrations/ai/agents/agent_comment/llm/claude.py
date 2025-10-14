import os
import json
import re

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from typing import List, Dict
from datetime import datetime, timezone

from app.comment.models import Comment, CommentAnalyzer, CommentQualityScore

load_dotenv()

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
        self.setup_prompts()
        self.setup_chains()

    def setup_prompts(self):
        """Sets up prompt templates."""

        # Review analysis prompt
        self.analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", """Sen bir e-ticaret uzmanısın. Ürün yorumlarını analiz ediyorsun. 
            Her yorum için JSON formatında analiz yapacaksın."""),
            ("human", """Aşağıdaki ürün yorumunu analiz et:

            Yorum: {review}

            Lütfen şu bilgileri JSON formatında ver:
            {{
                "sentiment": "pozitif/negatif/nötr",
                "sentiment_score": 0-10 arası puan,
                "category": "şikayet/övgü/soru/öneri/bilgi_talebi/ürün kalitesi/kargo/fiyat/hizmet/genel",
                "urgency": "düşük/orta/yüksek",
                "keywords": ["anahtar", "kelime", "listesi"],
                "summary": "yorumun kısa özeti",
                "main_issues": ["ana sorunlar listesi"],
                "requires_action": true/false,
                "response_tone": "formal/samimi/özür_dileyen/teşekkür_eden"
            }}

            Sadece JSON formatında cevap ver, başka açıklama ekleme.""")
        ])

        # Response generation prompt
        self.response_prompt = ChatPromptTemplate.from_messages([
            ("system", """Sen Türkiye'nin en büyük e-ticaret sitelerinden birinin profesyonel müşteri temsilcisisin.

            Görevin:
            - Müşteri yorumlarına samimi, profesyonel ve yardımsever cevaplar vermek
            - Türk müşteri hizmetleri kültürüne uygun davranmak
            - Şirketin imajını koruyarak müşteri memnuniyetini sağlamak

            Kuralların:
            - Herzaman Türkçe cevap ver
            - Müşteriyi "Değerli müşterimiz" diye hitap et
            - Şikayet durumunda samimi özür dile ve çözüm odaklı ol
            - Övgü durumunda içtenlikle teşekkür et
            - Soru durumunda detaylı ve faydalı bilgi ver
            - Çözüm önerilerini net ve uygulanabilir yap
            - 75-200 kelime arası cevap yaz
            - Profesyonel ama sıcak bir ton kullan"""),

            ("human", """Müşteri Bilgileri:
            - Müşteri: {customer_name}
            - Ürün: {product_name}
            - Yorum: {review}

            Yorum Analizi:
            {analysis}

            Bu bilgilere dayanarak müşteriye uygun bir cevap yaz. Müşterinin durumuna göre ton ve içeriği ayarla.""")
        ])

        # Quality control prompt
        self.quality_check_prompt = ChatPromptTemplate.from_messages([
            ("system", """Sen bir müşteri hizmetleri kalite kontrolcüsüsün.
            Müşteri temsilcilerinin yazdığı cevapları değerlendiriyorsun."""),
            ("human", """Orijinal Yorum: {review}

            Üretilen Cevap: {response}

            Bu cevabı değerlendir:
            1. Profesyonellik (1-10)
            2. Uygunluk (1-10)
            3. Samimilik (1-10)
            4. Çözüm odaklılık (1-10)
            5. Genel puan (1-10)

            JSON formatında değerlendirme ver ve gerekirse iyileştirme önerisi yap:
            {{
                "scores": {{
                    "professionalism": 8,
                    "relevance": 9,
                    "warmth": 7,
                    "solution_focus": 8,
                    "overall": 8
                }},
                "feedback": "kısa iyileştirme önerisi",
                "approved": true/false
            }}""")
        ])

    def setup_chains(self):
        """Sets up LangChain chains."""
        self.analysis_chain = LLMChain(
            llm=self.llm,
            prompt=self.analysis_prompt,
            verbose=False
        )

        self.response_chain = LLMChain(
            llm=self.llm,
            prompt=self.response_prompt,
            verbose=False
        )

        self.quality_chain = LLMChain(
            llm=self.llm,
            prompt=self.quality_check_prompt,
            verbose=False
        )

    def load_reviews_from_text(self, content: str) -> List[Dict]:
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
                        'rating': self.extract_rating('|'.join(parts[3:]) if len(parts) > 3 else "")
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
                        'rating': self.extract_rating(review)
                    })
                # Format 3: Only review
                else:
                    reviews.append({
                        'id': review_id,
                        'product': 'Not specified',
                        'customer': 'Anonymous Customer',
                        'review': ' '.join(lines),
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'rating': self.extract_rating(' '.join(lines))
                    })

                review_id += 1
        except Exception as e:
            print(f"Error: {e}")

        return reviews

    def extract_rating(self, text: str) -> int:
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

    def analyze_review(self, review: str) -> Dict:
        """Analyzes the review using Claude."""
        try:
            analysis_result = self.analysis_chain.run(review=review)

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

    def generate_response(self, review_data: Dict, analysis: Dict) -> str:
        """Generates a response for the review using Claude."""
        try:
            response = self.response_chain.run(
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

    def quality_check(self, review: str, response: str) -> Dict:
        """Checks the quality of the generated response."""
        try:
            quality_result = self.quality_chain.run(
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

    def process_all_reviews(self, content: str, enable_quality_check: bool = True) -> List[Dict]:
        """Processes all reviews and generates responses."""
        reviews = self.load_reviews_from_text(content)
        results = []

        for i, review_data in enumerate(reviews, 1):
            analysis = self.analyze_review(review_data['review'])

            if 'error' not in analysis:
                response = self.generate_response(review_data, analysis)
                quality = {}

                if enable_quality_check:
                    quality = self.quality_check(review_data['review'], response)

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

    def save_results(self, id: int, results: List[Dict], output_file: str = "review_responses.txt"):
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
        agent.save_results(id, results, "claude_review_responses3.txt")
    except Exception as e:
        print(f"Error: {e}")
