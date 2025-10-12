import json
import os
from typing import Dict, List
from langchain.llms import Anthropic
from langchain.chat_models import ChatAnthropic
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.schema import BaseOutputParser
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv


load_dotenv()


class CommentAnalysisParser(BaseOutputParser):
    """Yorum analizi çıktısını parse eden sınıf"""

    def parse(self, text: str) -> Dict:
        """LLM çıktısını dict formatına çevir"""
        try:
            # Basit parsing - gerçek projede daha sofistike olabilir
            lines = text.strip().split('\n')
            result = {}

            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    result[key.strip().lower()] = value.strip()

            return result
        except Exception as e:
            return {"error": f"Parsing hatası: {str(e)}"}


class ResponseParser(BaseOutputParser):
    """Cevap çıktısını parse eden sınıf"""

    def parse(self, text: str) -> str:
        """LLM çıktısından temiz cevap çıkar"""
        # Gereksiz açıklamaları temizle
        response = text.strip()
        if response.startswith('"') and response.endswith('"'):
            response = response[1:-1]
        return response


class ECommerceCommentProcessor:
    """Ana işlem sınıfı - LangChain chains'lerini yönetir"""

    def __init__(self):
        # Claude LLM initialize
        self.llm = ChatAnthropic(
            model="claude-3-7-sonnet-20250219",
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            temperature=0.3
        )

        self.analysis_parser = CommentAnalysisParser()
        self.response_parser = ResponseParser()

        # Chain'leri oluştur
        self._create_chains()

    def _create_chains(self):
        """LangChain chain'lerini oluştur"""

        # 1. ANALYSIS CHAIN - Yorum Analizi
        analysis_prompt = ChatPromptTemplate.from_template("""
        Sen e-ticaret yorumlarında uzman bir analistsin. 
        Aşağıdaki yorumu analiz et ve şu formatta çıktı ver:

        Yorum: {comment}

        Analiz et:
        Sentiment: (Pozitif/Negatif/Nötr)
        Kategori: (Ürün Kalitesi/Kargo/Fiyat/Hizmet/Genel)
        Önem: (Yüksek/Orta/Düşük)  
        Aciliyet: (Var/Yok)
        Anahtar Kelimeler: (virgülle ayır)
        """)

        self.analysis_chain = LLMChain(
            llm=self.llm,
            prompt=analysis_prompt,
            output_key="analysis_result",
            output_parser=self.analysis_parser
        )

        # 2. RESPONSE GENERATION CHAIN - Cevap Üretme
        response_prompt = ChatPromptTemplate.from_template("""
        Sen Trendyol'da satış yapan bir mağazanın müşteri hizmetleri uzmanısın.

        Orijinal Yorum: {comment}
        Analiz Sonucu: {analysis_result}

        Bu yoruma SADECE cevap metnini yaz. Başka açıklama yapma.

        KURALLAR:
        - Maksimum 2-3 cümle
        - Türkçe, samimi ama profesyonel
        - Şikayet varsa çözüm odaklı
        - Teşekkür varsa minnettarlık göster
        - Trendyol satıcısı kimliğiyle yaz

        CEVAP:
        """)

        self.response_chain = LLMChain(
            llm=self.llm,
            prompt=response_prompt,
            output_key="generated_response",
            output_parser=self.response_parser
        )

        # 3. SEQUENTIAL CHAIN - İki chain'i sırayla çalıştır
        self.full_chain = SequentialChain(
            chains=[self.analysis_chain, self.response_chain],
            input_variables=["comment"],
            output_variables=["analysis_result", "generated_response"],
            verbose=True
        )

    def process_single_comment(self, comment: str) -> Dict:
        """Tek yorum işle"""
        try:
            result = self.full_chain({"comment": comment})

            return {
                "orijinal_yorum": comment,
                "analiz": result["analysis_result"],
                "uretilen_cevap": result["generated_response"]
            }
        except Exception as e:
            return {
                "orijinal_yorum": comment,
                "hata": f"İşlem hatası: {str(e)}"
            }

    def process_comments_from_file(self, input_file: str, output_file: str):
        """JSON dosyasından yorumları işle"""

        # Input dosyasını oku
        with open(input_file, 'r', encoding='utf-8') as f:
            comments_data = json.load(f)

        all_results = []

        print("🚀 LangChain ile yorum işleme başladı...")
        print("-" * 60)

        for i, comment_item in enumerate(comments_data, 1):
            comment_text = comment_item.get('yorum', '')

            print(f"📝 İşleniyor ({i}/{len(comments_data)}): {comment_text[:50]}...")

            # Yorumu işle
            result = self.process_single_comment(comment_text)
            all_results.append(result)

            if 'hata' not in result:
                print(f"✅ Analiz: {str(result['analiz'])[:100]}...")
                print(f"💬 Cevap: {result['uretilen_cevap']}")
            else:
                print(f"❌ Hata: {result['hata']}")

            print("-" * 60)

        # Output dosyasına kaydet
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)

        print(f"✅ Tüm sonuçlar {output_file} dosyasına kaydedildi!")
        return all_results


# TOOLS - LangChain Agent için (opsiyonel)
def get_response_templates():
    """Cevap şablonlarını döndür"""
    templates = {
        "pozitif": ["Teşekkürler!", "Memnuniyetiniz güzel!"],
        "negatif": ["Özür dileriz", "Sorunu çözeceğiz"],
        "kargo": ["Kargo gecikmesi için özür dileriz"],
    }
    return str(templates)


# Agent tools tanımla
tools = [
    Tool(
        name="ResponseTemplates",
        func=get_response_templates,
        description="E-ticaret cevap şablonlarını getir"
    )
]


def run_with_agent_approach(comments_file: str):
    """Agent yaklaşımı ile çalıştır (alternatif)"""

    llm = ChatAnthropic(
        model="claude-3-7-sonnet-20250219",
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
    )

    memory = ConversationBufferMemory(memory_key="chat_history")

    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=True
    )

    # Yorumları oku ve agent ile işle
    with open(comments_file, 'r', encoding='utf-8') as f:
        comments = json.load(f)

    for comment_item in comments:
        comment = comment_item['yorum']

        prompt = f"""
        Bu e-ticaret yorumunu analiz et ve profesyonel cevap üret:
        "{comment}"

        1. Önce sentiment ve kategori belirle
        2. Sonra uygun cevap üret
        """

        response = agent.run(prompt)
        print(f"Yorum: {comment}")
        print(f"Agent Cevabı: {response}")
        print("-" * 80)


def main():
    """Ana fonksiyon"""

    # Dosya yolları
    input_file = "../../../integrations/ai/agents/agent_comment/data/yorumlar.json"
    output_file = "output/langchain_cevaplar.json"

    # İşlemci oluştur
    processor = ECommerceCommentProcessor()

    # Yorumları işle
    results = processor.process_comments_from_file(input_file, output_file)

    print(f"\n🎉 Toplam {len(results)} yorum işlendi!")


if __name__ == "__main__":
    main()