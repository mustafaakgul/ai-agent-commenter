from datetime import datetime
from typing import List, Dict


def load_reviews_from_file(self, file_path: str) -> List[Dict]:
    """Txt dosyasından yorumları yükler - Geliştirilmiş format desteği"""
    reviews = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()

        # Boş satırlarla ayrılmış blokları destekle
        content = file_path
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
