# E-ticaret Yorum Cevaplama AI Agent - Claude ile
import os

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, SystemMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
import re
from typing import List, Dict
from datetime import datetime


# load_dotenv()


class ECommerceReviewAgent:
    def __init__(self, anthropic_api_key: str = None, model_name: str = "claude-3-sonnet-20240229"):
        """E-ticaret yorum cevaplama agent'ini Claude ile başlatır"""
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
        """Prompt şablonlarını ayarlar"""

        # Yorum analiz prompt'u
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

        # Cevap üretme prompt'u
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

        # Kalite kontrol prompt'u
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
        """LangChain zincirlerini ayarlar"""
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

        """
          # 3. SEQUENTIAL CHAIN - İki chain'i sırayla çalıştır
        self.full_chain = SequentialChain(
            chains=[self.analysis_chain, self.response_chain],
            input_variables=["comment"],
            output_variables=["analysis_result", "generated_response"],
            verbose=True
        )
        """

    def load_reviews_from_file(self, file_path: str) -> List[Dict]:
        """Txt dosyasından yorumları yükler - Geliştirilmiş format desteği"""
        reviews = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()

            # Boş satırlarla ayrılmış blokları destekle
            blocks = content.split('\n\n')

            review_id = 1
            for block in blocks:
                lines = [line.strip() for line in block.split('\n') if line.strip()]

                if len(lines) == 0:
                    continue

                # Format 1: "Ürün|Müşteri|Yorum"
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

                # Format 2: Çok satırlı format
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

                # Format 3: Sadece yorum
                else:
                    reviews.append({
                        'id': review_id,
                        'product': 'Belirtilmemiş',
                        'customer': 'Anonim Müşteri',
                        'review': ' '.join(lines),
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'rating': self.extract_rating(' '.join(lines))
                    })

                review_id += 1

        except FileNotFoundError:
            print(f"❌ Dosya bulunamadı: {file_path}")
        except Exception as e:
            print(f"❌ Dosya okuma hatası: {e}")

        return reviews

    def extract_rating(self, text: str) -> int:
        """Metinden yıldız puanı çıkarmaya çalışır"""
        rating_patterns = [
            r'(\d+)\s*yıldız',
            r'(\d+)\s*/\s*5',
            r'(\d+)\s*/\s*10',
            r'⭐' * 5,  # Yıldız emoji sayısı
        ]

        for pattern in rating_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))

        # Emoji yıldızları say
        star_count = text.count('⭐')
        if star_count > 0:
            return min(star_count, 5)

        return 0  # Puan bulunamadı

    def analyze_review(self, review: str) -> Dict:
        """Yorumu Claude ile analiz eder"""
        try:
            print("🔍 Yorum analiz ediliyor...")
            analysis_result = self.analysis_chain.run(review=review)

            # JSON parsing yap
            try:
                # Bazen Claude extra açıklama ekleyebilir, sadece JSON kısmını al
                json_start = analysis_result.find('{')
                json_end = analysis_result.rfind('}') + 1
                if json_start != -1 and json_end != -1:
                    json_str = analysis_result[json_start:json_end]
                    analysis = json.loads(json_str)
                else:
                    raise ValueError("JSON bulunamadı")

            except (json.JSONDecodeError, ValueError) as e:
                print(f"⚠️ JSON parse hatası, varsayılan analiz kullanılıyor: {e}")
                analysis = {
                    "sentiment": "nötr",
                    "sentiment_score": 5,
                    "category": "genel",
                    "urgency": "orta",
                    "keywords": ["müşteri", "yorumu"],
                    "summary": review[:100] + "..." if len(review) > 100 else review,
                    "main_issues": ["analiz edilemedi"],
                    "requires_action": True,
                    "response_tone": "samimi"
                }

            return analysis

        except Exception as e:
            print(f"❌ Analiz hatası: {e}")
            return {"error": str(e)}

    def generate_response(self, review_data: Dict, analysis: Dict) -> str:
        """Yorum için Claude ile cevap üretir"""
        try:
            print("✍️ Cevap üretiliyor...")

            response = self.response_chain.run(
                customer_name=review_data['customer'],
                product_name=review_data['product'],
                review=review_data['review'],
                analysis=json.dumps(analysis, ensure_ascii=False, indent=2)
            )

            return response.strip()

        except Exception as e:
            print(f"❌ Cevap üretme hatası: {e}")
            return """Değerli müşterimiz,

            Yorumunuz için teşekkür ederiz. Şu anda sistemimizde geçici bir sorun yaşanmaktadır. 
            Lütfen daha sonra tekrar deneyin veya müşteri hizmetlerimizle iletişime geçin.

            Saygılarımızla,
            Müşteri Hizmetleri"""

    def quality_check(self, review: str, response: str) -> Dict:
        """Üretilen cevabın kalitesini kontrol eder"""
        try:
            print("🔍 Kalite kontrolü yapılıyor...")
            quality_result = self.quality_chain.run(
                review=review,
                response=response
            )

            # JSON parsing
            try:
                json_start = quality_result.find('{')
                json_end = quality_result.rfind('}') + 1
                if json_start != -1 and json_end != -1:
                    json_str = quality_result[json_start:json_end]
                    quality = json.loads(json_str)
                else:
                    raise ValueError("JSON bulunamadı")
            except:
                quality = {
                    "scores": {
                        "professionalism": 7,
                        "relevance": 7,
                        "warmth": 7,
                        "solution_focus": 7,
                        "overall": 7
                    },
                    "feedback": "Kalite kontrolü yapılamadı",
                    "approved": True
                }

            return quality

        except Exception as e:
            print(f"⚠️ Kalite kontrol hatası: {e}")
            return {"error": str(e)}

    def process_all_reviews(self, file_path: str, enable_quality_check: bool = True) -> List[Dict]:
        """Tüm yorumları işler ve cevaplar üretir"""
        reviews = self.load_reviews_from_file(file_path)
        results = []

        print(f"🚀 Toplam {len(reviews)} yorum işleniyor...\n")

        for i, review_data in enumerate(reviews, 1):
            print(f"📝 İşleniyor {i}/{len(reviews)}: {review_data['customer']}")
            print(f"📦 Ürün: {review_data['product']}")
            print(f"💬 Yorum: {review_data['review'][:100]}{'...' if len(review_data['review']) > 100 else ''}")

            # Yorumu analiz et
            analysis = self.analyze_review(review_data['review'])

            if 'error' not in analysis:
                # Cevap üret
                response = self.generate_response(review_data, analysis)

                # Kalite kontrolü (opsiyonel)
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
                    'generated_response': "Analiz hatası nedeniyle cevap üretilemedi.",
                    'quality_check': {},
                    'processed_at': datetime.now().isoformat()
                }

            results.append(result)
            print("✅ Tamamlandı\n" + "-" * 50 + "\n")

        return results

    def save_results(self, results: List[Dict], output_file: str = "review_responses.txt"):
        """Sonuçları detaylı formatta dosyaya kaydeder"""
        try:
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write("🛒 E-TİCARET YORUM CEVAPLARI - CLAUDE AI\n")
                file.write("=" * 60 + "\n")
                file.write(f"📅 Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write(f"📊 Toplam İşlenen Yorum: {len(results)}\n")
                file.write("=" * 60 + "\n\n")

                for i, result in enumerate(results, 1):
                    original = result['original']
                    analysis = result['analysis']
                    response = result['generated_response']
                    quality = result.get('quality_check', {})

                    file.write(f"📝 YORUM #{i}\n")
                    file.write("─" * 40 + "\n")
                    file.write(f"👤 Müşteri: {original['customer']}\n")
                    file.write(f"📦 Ürün: {original['product']}\n")
                    file.write(f"⭐ Puan: {original.get('rating', 'N/A')}\n")
                    file.write(f"📅 Tarih: {original['date']}\n\n")

                    file.write("💬 ORİJİNAL YORUM:\n")
                    file.write(f"{original['review']}\n\n")

                    if 'error' not in analysis:
                        file.write("🔍 ANALİZ:\n")
                        file.write(
                            f"• Duygu: {analysis.get('sentiment', 'N/A')} ({analysis.get('sentiment_score', 'N/A')}/10)\n")
                        file.write(f"• Kategori: {analysis.get('category', 'N/A')}\n")
                        file.write(f"• Aciliyet: {analysis.get('urgency', 'N/A')}\n")
                        file.write(f"• Anahtar Kelimeler: {', '.join(analysis.get('keywords', []))}\n")
                        file.write(f"• Özet: {analysis.get('summary', 'N/A')}\n")
                        file.write(f"• Ana Sorunlar: {', '.join(analysis.get('main_issues', []))}\n")
                        file.write(
                            f"• Aksiyon Gerekli: {'Evet' if analysis.get('requires_action', False) else 'Hayır'}\n\n")

                    file.write("✍️ ÜRETİLEN CEVAP:\n")
                    file.write(f"{response}\n\n")

                    if quality and 'scores' in quality:
                        file.write("🏆 KALİTE PUANI:\n")
                        scores = quality['scores']
                        file.write(f"• Profesyonellik: {scores.get('professionalism', 'N/A')}/10\n")
                        file.write(f"• Uygunluk: {scores.get('relevance', 'N/A')}/10\n")
                        file.write(f"• Samimilik: {scores.get('warmth', 'N/A')}/10\n")
                        file.write(f"• Çözüm Odaklılık: {scores.get('solution_focus', 'N/A')}/10\n")
                        file.write(f"• Genel Puan: {scores.get('overall', 'N/A')}/10\n")
                        file.write(f"• Onaylandı: {'✅ Evet' if quality.get('approved', False) else '❌ Hayır'}\n")
                        if quality.get('feedback'):
                            file.write(f"• Geri Bildirim: {quality['feedback']}\n")
                        file.write("\n")

                    file.write("=" * 60 + "\n\n")

            print(f"✅ Sonuçlar {output_file} dosyasına kaydedildi.")

        except Exception as e:
            print(f"❌ Dosya kaydetme hatası: {e}")


def create_sample_reviews_file():
    """Geliştirilmiş örnek yorumlar dosyası oluşturur"""
    sample_content = """Ürün resimlerinizde FDA onaylı yazıyor ancak ürün etikerinde FDa ibaresi yok. Şirketiniz FDa ya kayitli mi?"""

    with open("sample_reviews2.txt", "w", encoding="utf-8") as file:
        file.write(sample_content)
    print("📝 sample_reviews2.txt örnek dosyası oluşturuldu.")


# Kullanım örneği
if __name__ == "__main__":
    print("🚀 E-Ticaret Yorum Cevaplama AI Agent (Claude) başlatılıyor...\n")

    # Anthropic API key'inizi buraya girin veya environment variable olarak ayarlayın
    API_KEY = "your_anthropic_api_key_here"

    # Örnek dosya oluştur
    create_sample_reviews_file()

    try:
        # Agent'i başlat
        print("🤖 Claude AI bağlantısı kuruluyor...")
        agent = ECommerceReviewAgent(
            anthropic_api_key=API_KEY,
            model_name="claude-3-5-sonnet-20241022"  # veya claude-3-opus-20240229, anthropic/claude-3-5-sonnet-20240620
        )

        # Yorumları işle
        print("📊 Yorumlar işleniyor...\n")
        results = agent.process_all_reviews(
            file_path="sample_reviews2.txt",
            enable_quality_check=True  # Kalite kontrolünü açık tut
        )

        # Sonuçları kaydet
        agent.save_results(results, "claude_review_responses4.txt")

        print("\n🎉 İşlem tamamlandı!")

    except Exception as e:
        print(f"❌ Genel hata: {e}")
        # print("🔧 API key'inizi kontrol edin ve tekrar deneyin.")
