import json
from crewai import Agent, Task, Crew
from crewai.llm import LLM
# from tools.response_template_loader import ResponseTemplateLoader


def load_comments_from_json(file_path):
    """JSON dosyasından yorumları yükle"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


# def save_responses_to_json(responses, output_file):
#     """Üretilen cevapları JSON dosyasına kaydet"""
#     with open(output_file, 'w', encoding='utf-8') as file:
#         json.dump(responses, file, ensure_ascii=False, indent=2)

def save_responses_to_json(responses, output_file):
    """Üretilen cevapları JSON dosyasına kaydet"""
    # TaskOutput nesnelerini string'e çevir
    serializable_responses = []
    for response in responses:
        serializable_response = {
            "orijinal_yorum": response["orijinal_yorum"],
            "analiz": response["analiz"].raw if hasattr(response["analiz"], 'raw') else str(response["analiz"]),
            "uretilen_cevap": response["uretilen_cevap"].raw if hasattr(response["uretilen_cevap"], 'raw') else str(
                response["uretilen_cevap"])
        }
        serializable_responses.append(serializable_response)

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(serializable_responses, file, ensure_ascii=False, indent=2)


# AGENT 1: Yorum Analizcisi
comment_analyzer = Agent(
    role="Yorum Analizcisi",
    goal="E-ticaret yorumlarını analiz et ve kategorize et",
    backstory="""Sen e-ticaret yorumlarında uzman bir analistsin. 
                 Müşteri yorumlarının duygusal tonunu, kategorisini ve 
                 önem derecesini belirlemekte çok iyisin.""",
    tools=[],
    llm=LLM(
        model="anthropic/claude-3-5-sonnet-20240620",

        temperature=0.7,
        max_tokens=512
    ),
    verbose=True
)

# AGENT 2: Cevap Üreticisi
response_generator = Agent(
    role="Müşteri Hizmetleri Uzmanı",
    goal="Yorumlara profesyonel ve empatik cevaplar üret",
    backstory="""Sen Trendyol'da satış yapan bir mağazanın 
                 müşteri hizmetleri uzmanısın. Türkçe, samimi 
                 ama profesyonel yanıtlar veriyorsun. Müşteri 
                 memnuniyetini artırmak senin önceliğin.""",
    llm=LLM(
        model="anthropic/claude-3-5-sonnet-20240620",

        temperature=0.7,
        max_tokens=512
    ),
    # tools=[ResponseTemplateLoader()],
    verbose=True
)


def process_comments(comments_file, output_file):
    """Yorumları işle ve cevaplar üret"""

    # JSON dosyasından yorumları yükle
    comments_data = load_comments_from_json(comments_file)

    all_responses = []

    for comment_item in comments_data:
        comment_text = comment_item.get('yorum', '')

        # TASK 1: Yorum Analizi
        analyze_task = Task(
            description=f"""
            Bu e-ticaret yorumunu detaylıca analiz et:

            Yorum: "{comment_text}"

            Şu kriterlere göre değerlendir:
            - Sentiment (Pozitif/Negatif/Nötr)
            - Kategori (Ürün Kalitesi/Kargo/Fiyat/Hizmet/Genel)
            - Önem Derecesi (Yüksek/Orta/Düşük)
            - Aciliyeti var mı (Şikayet/İade/Sorun)
            """,
            expected_output="JSON formatında analiz sonuçları",
            agent=comment_analyzer
        )

        # TASK 2: Cevap Üretme
        response_task = Task(
            description=f"""
            Analiz sonuçlarını kullanarak bu yoruma profesyonel cevap üret:

            Yorum: "{comment_text}"

            KURALLAR:
            - Maksimum 2-3 cümle
            - Samimi ve profesyonel ton kullan
            - Şikayet varsa çözüm odaklı yaklaşım sergile
            - Teşekkür varsa minnettarlık göster
            - Özür gerekiyorsa samimi özür dile
            - Trendyol satıcısı kimliğiyle yaz
            """,
            expected_output="Profesyonel müşteri yanıtı",
            agent=response_generator,
            context=[analyze_task]
        )

        # Crew oluştur ve çalıştır
        crew = Crew(
            agents=[comment_analyzer, response_generator],
            tasks=[analyze_task, response_task],
            verbose=True
        )

        # İşlemi çalıştır
        result = crew.kickoff()

        # Sonucu kaydet
        response_data = {
            "orijinal_yorum": comment_text,
            "analiz": analyze_task.output,
            "uretilen_cevap": response_task.output
        }

        all_responses.append(response_data)

        print(f"✅ İşlendi: {comment_text[:50]}...")
        print(f"📝 Cevap: {response_task.output}")
        print("-" * 80)
        print(response_data)

    # Tüm cevapları dosyaya kaydet
    # save_responses_to_json(all_responses, output_file)
    print(f"✅ Tüm cevaplar {output_file} dosyasına kaydedildi!")


if __name__ == "__main__":
    # Dosya yolları
    input_file = "../../../integrations/ai/agents/agent_comment/data/yorumlar.json"
    output_file = "../../../integrations/ai/agents/agent_comment/output/cevaplar.json"

    # İşlemi başlat
    process_comments(input_file, output_file)