from crewai_tools import tool


@tool
def ResponseTemplateLoader():
    """E-ticaret yorumları için hazır cevap şablonları"""

    templates = {
        "pozitif_tesekkur": [
            "Memnuniyetiniz bizim için çok değerli! Teşekkür ederiz. 🙏",
            "Güzel yorumunuz için çok teşekkürler! Sizleri mutlu etmek bizim önceliğimiz.",
            "Beğenmenize sevindik! Desteğiniz için minnettarız."
        ],

        "negatif_sikayet": [
            "Yaşadığınız sorun için özür dileriz. Lütfen bizimle iletişime geçin, sorunu çözelim.",
            "Memnuniyetsizliğiniz bizi üzdü. Konuyu acilen inceleyip geri dönüş yapacağız.",
            "Özür dileriz! Lütfen mesaj atın, sorunu hemen çözmek istiyoruz."
        ],

        "kargo_problemi": [
            "Kargo gecikmesi için özür dileriz. Kargo süreçlerimizi gözden geçiriyoruz.",
            "Kargo sorunu için üzgünüz. Kargo firmamızla görüştük, bu tür gecikmeler tekrarlanmayacak.",
            "Kargo konusundaki yaşadığınız sıkıntı için samimi özürlerimizi sunarız."
        ],

        "urun_kalitesi": [
            "Ürün kalitesi konusundaki geri bildiriminiz için teşekkürler. Kalite kontrol süreçlerimizi güçlendiriyoruz.",
            "Kalite beklentinizi karşılayamadığımız için özür dileriz. İade sürecini başlatabilirsiniz.",
            "Ürün kalitesi ile ilgili yaşadığınız sorun için özür dileriz."
        ],

        "genel_notr": [
            "Değerli geri bildiriminiz için teşekkürler.",
            "Yorumunuz için teşekkür ederiz. Görüşleriniz bizim için önemli.",
            "Geri bildiriminizi dikkate alacağız. Teşekkürler."
        ]
    }

    return templates
