import joblib
import pandas as pd

# Eğitilen modeli sistemden yükle
model = joblib.load("model.pkl")

# Test etmek istediğin yeni adayın bilgileri
deneyim_yili = 5
egitim_seviyesi = 3  # 1, 2 veya 3
skill_puani = 8
test_skoru_puani = 80

# DİKKAT: DataFrame sütun isimleri ml.py modelindekiyle BİREBİR aynı sırada ve isimde olmalı!
girdi = pd.DataFrame(
    [[deneyim_yili, egitim_seviyesi, skill_puani, test_skoru_puani]],
    columns=["deneyim", "egitim", "skill", "test_skoru"]
)

# Tahmin algoritmasını çalıştır
sonuc = model.predict(girdi)

print(f"\nAdayın İşe Alım Durumu Tahmini: {sonuc[0].upper()}")