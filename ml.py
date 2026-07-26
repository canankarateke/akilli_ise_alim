import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score #çapraz kararlılık testi için
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix #detaylı rapor için
import joblib #verileri kaydetmek için 

# 1. Yeni veri setini yükle 
data = pd.read_csv("dataset.csv", encoding="utf-8", sep=";")
data.columns = data.columns.str.strip()  # Gizli boşlukları temizler

# 2. X (Girdiler) ve y (Hedef Etiket) olarak ayır
X = data.drop(columns=["etiket"])
y = data["etiket"]

# 3. Eğitim/Test bölmesi (%20 Test, %80 Eğitim)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)# starfity y verileri orantılı böler test ve antrenman için

# 4. Model Tanımlama (Ezberlemeyi ve kararsızlığı önleyen korumalı parametreler)
model = RandomForestClassifier(
    n_estimators=150,
    max_depth=5,
    min_samples_leaf=5,
    class_weight="balanced",# verilerdeki sayısal dengesizlikleri kaldırmak için kullanılıyor
    random_state=42 # algoritma her çalıştığında rastgele seçilen %20lik %80lik kısımların aynı çoıkmasını sağlar 
)

# 5. Modeli Eğit
model.fit(X_train, y_train)

# 6. Başarı Oranını Yazdır
accuracy = model.score(X_test, y_test)
print(f"Test doğruluk oranı: %{accuracy*100:.2f}")

# 7. Detaylı Performans Raporları
y_pred = model.predict(X_test)
print("\n--- Confusion Matrix ---")
print(confusion_matrix(y_test, y_pred))
print("\n--- Classification Report ---")
print(classification_report(y_test, y_pred))

# 8. Cross-Validation (5 Katmanlı Kararlılık Kontrolü)
scores = cross_val_score(model, X, y, cv=5)
print("\nCross-validation doğrulukları:", scores)
print("Ortalama doğruluk:", scores.mean())

# 9. Modeli İleride Kullanmak Üzere Kaydet
joblib.dump(model, "model.pkl")
print("\nModel başarıyla kaydedildi: model.pkl")
# Modelin hangi sütuna ne kadar önem verdiğini gösterir
for col, imp in zip(X.columns, model.feature_importances_):
    print(f"{col}: {imp}")