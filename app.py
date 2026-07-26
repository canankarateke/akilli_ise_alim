from flask import Flask, render_template, request, jsonify
import joblib
from flask_cors import CORS
import numpy as np
import os

from database import get_db_connection, init_db, save_user, check_user

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'backend_projesi_gizli_anahtari'
CORS(app)

# MODEL YÜKLEME
MODEL_PATH = 'model.pkl'
model = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

# SAYFA ROTALARI
@app.route('/')
def ana_sayfa():
    return render_template('index.html')

@app.route('/giris')
def giris_sayfasi():
    return render_template('login.html')

@app.route('/kaydol')
def kaydol_sayfasi():
    return render_template('register.html')


# ==========================================
#  API ENDPOINTLERİ
# ==========================================

@app.route('/api/tahmin', methods=['POST'])
def api_tahmin():
    if model is None:
        return jsonify({'durum': 'hata', 'mesaj': 'Model hazır değil'}), 500
    
    data = request.get_json()
    
    isim = data.get('isim', 'İsimsiz Aday')
    deneyim = int(data['deneyim'])
    
    # DÜZELTME: Frontend zaten 1, 2, 3, 4 sayılarını gönderiyor. 
    # Direkt gelen sayıyı int tipine çevirip alıyoruz, sözlüğe gerek yok.
    try:
        egitim = int(data.get('egitim', 2))
    except:
        egitim = 2
        
    skill = int(data['skill'])
    test_skoru = int(data['test_skoru'])
    
    # Modelin tam eğitildiği formata uygun numpy array girdisi
    girdi = np.array([[deneyim, egitim, skill, test_skoru]], dtype=np.int64)
    
    # Modelin 'Uygun (1)' olma ihtimalini doğrudan çekiyoruz.
    olasiliklar = model.predict_proba(girdi)[0]
    skor_orani = float(olasiliklar[1])
    
    if skor_orani >= 0.50:
        sonuc_etiket = "Uygun"
    else:
        sonuc_etiket = "Red"

    # Veritabanına kayıt
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO adaylar (isim, deneyim, egitim, skill, test_skoru, tahmin_sonucu)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (isim, deneyim, egitim, skill, test_skoru, sonuc_etiket))
    conn.commit()
    conn.close()
    
    return jsonify({
        'durum': sonuc_etiket, 
        'skor': skor_orani
    })

# API - KAYDOL
@app.route('/api/kaydol', methods=['POST'])
def api_kaydol():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if not email or not username or not password:
        return jsonify({'durum': 'hata', 'mesaj': 'Lütfen tüm alanları doldurun!'}), 400

    try:
        save_user(email, username, password)
        return jsonify({'durum': 'başarılı', 'mesaj': 'Kullanıcı başarıyla kaydedildi!'})
    except Exception as e:
        return jsonify({'durum': 'hata', 'mesaj': str(e)}), 400

# API - GİRİŞ
@app.route('/api/giris', methods=['POST'])
def api_giris():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'durum': 'hata', 'mesaj': 'Lütfen alanları doldurun!'}), 400

    if check_user(username, password):
        # DÜZELTME: Frontend'in düzgün çalışması ve hata vermemesi için token ve kullanıcı adını geri döndürüyoruz.
        return jsonify({
            'durum': 'başarılı', 
            'mesaj': 'Giriş başarılı!',
            'token': 'ornek_jwt_token_backend_entegrasyonu',
            'username': username
        })
    else:
        return jsonify({'durum': 'hata', 'mesaj': 'Hatalı kullanıcı adı veya şifre!'}), 401

# API - GEÇMİŞ KAYITLAR
@app.route('/api/gecmis', methods=['GET'])
def api_gecmis():
    try:
        conn = get_db_connection()
        # DÜZELTME: SQL sorgusuna 'egitim' kolonu eklendi!
        satirlar = conn.execute(
            'SELECT id, isim, deneyim, egitim, test_skoru, tahmin_sonucu FROM adaylar ORDER BY id DESC'
        ).fetchall()
        conn.close()
        
        # DÜZELTME: JSON paketinin içine "egitim" anahtarı ve verisi eklendi!
        liste = [
            {
                "id": r["id"], 
                "isim": r["isim"], 
                "deneyim": f"{r['deneyim']} Yıl",
                "egitim": r["egitim"], # Artık React bu veriyi görebilecek!
                "skor": r["test_skoru"], 
                "durum": r["tahmin_sonucu"]
            }
            for r in satirlar
        ]
        return jsonify(liste)
    except Exception as e:
        return jsonify([]), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)