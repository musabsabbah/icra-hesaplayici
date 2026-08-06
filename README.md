# İcra Takip & Dosya Kapak Hesabı

FastAPI ve Tailwind CSS kullanılarak geliştirilmiş, gelişmiş faiz, harç ve masraf hesaplama paneli.

## 🚀 Özellikler

- **Esnek Faiz Seçenekleri:** Yasal (Kanuni), Avans (Ticari), Akdi ve Mevduat faizi hesaplama.
- **Faiz Tipleri:** Kademeli (değişken) oranlı veya sabit oranlı faiz hesabı.
- **Dinamik Harç & Masraf Yönetimi:** Seçimlik başvurma harcı, peşin harç, tahsil harcı safhaları (%4.55, %9.10, %11.38), tebligat masrafı ve AAÜT vekalet ücreti hesaplama.
- **Şeffaf Hesaplama:** Yalnızca seçilen harç kalemlerini toplam borca yansıtma ve detaylı döküm sunma.

## 🛠️ Kurulum ve Çalıştırma

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları takip edin:

```bash
# 1. Depoyu klonlayın
git clone [https://github.com/musabsabbah/icra-hesaplayici.git](https://github.com/musabsabbah/icra-hesaplayici.git)
cd icra-hesaplayici

# 2. Sanal ortam (venv) oluşturun ve aktifleştirin
python -m venv venv
source venv/bin/activate  # Windows için: venv\Scripts\activate

# 3. Gerekli paketleri yükleyin
pip install fastapi uvicorn jinja2 pydantic

# 4. Sunucuyu başlatın
uvicorn app:app --reload
```

Uygulama çalıştıktan sonra tarayıcınızdan **http://127.0.0.1:8000** adresine giderek kullanmaya başlayabilirsiniz.
