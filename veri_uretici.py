import numpy as np
import pandas as pd

# Her çalıştığında aynı rastgele verilerin üretilmesi için
np.random.seed(42)

ornek_sayisi = 1000

deneyim = np.random.randint(0, 11, size=ornek_sayisi)  # 0-10 yıl arası deneyim
egitim = np.random.randint(1, 5, size=ornek_sayisi)    
skill = np.random.randint(0, 16, size=ornek_sayisi)    # 1-10 arası yetenek skoru

# 2. Test skorunu yetenek ve eğitime bağlı ve gerçekçi kılalım
test_skoru = []
for i in range(ornek_sayisi):
    taban_skor = 40 + (skill[i] * 3) + (egitim[i] * 5)
    skor = taban_skor + np.random.randint(-10, 11)
    skor = np.clip(skor, 30, 100)  # Skor 30 ile 100 arasında kalmalı
    test_skoru.append(int(skor))

test_skoru = np.array(test_skoru)

# 3. Görselindeki gibi 'uygun' ve 'degil' etiketlerini mantıklı bir kurala bağlayalım
etiket = []
for i in range(ornek_sayisi):
    # İşe alım puanı hesaplama formülü
    toplam_puan = (deneyim[i] * 6) + (egitim[i] * 8) + (skill[i] * 5) + (test_skoru[i] * 0.5)
    
    # Eğer toplam puan barajın üzerindeyse 'uygun', altındaysa 'degil'
    if toplam_puan >= 90:
        etiket.append("uygun")
    else:
        etiket.append("degil")

# 4. Verileri DataFrame yapısında birleştirme
data_sentetik = pd.DataFrame({
    "deneyim": deneyim,
    "egitim": egitim,
    "skill": skill,
    "test_skoru": test_skoru,
    "etiket": etiket
})

# 5. Dosyayı  noktalı virgül formatında kaydedelim
data_sentetik.to_csv("dataset.csv", index=False, sep=";")

print("--- Sentetik Veri Seti Başarıyla Oluşturuldu ---")
print(f"Toplam Satır Sayısı: {len(data_sentetik)}")
print(data_sentetik['etiket'].value_counts())