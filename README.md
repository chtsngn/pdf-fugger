# PDFugger

PDF belgelerinizi eskitme efekti ile işleyen bir web uygulaması. Bu uygulama, modern PDF belgelerinizi taranmış gibi görünecek şekilde dönüştürür.

## Özellikler

- PDF sayfalarını görüntülere dönüştürme
- Mürekkep lekesi efekti ekleme
- Bulanıklık ayarı
- Yazı solukluğu kontrolü
- Sürükle-bırak dosya yükleme
- Gerçek zamanlı önizleme
- Ayarlanabilir filtre parametreleri
- Tam ekran PDF görüntüleme
- Otomatik dosya indirme

## Teknolojiler

### Backend
- Python 3.9
- Flask
- PyPDF2
- Pillow
- pdf2image

### Frontend
- Vue 3
- Vite
- TypeScript
- Tailwind CSS

### Deployment
- Docker
- Docker Compose

## Kurulum ve Çalıştırma

### Ön Gereksinimler
- Docker
- Docker Compose

### 1. Projeyi Klonlama
```bash
git clone https://github.com/kullaniciadi/pdf-fugger.git
cd pdf-fugger
```

### 2. Docker ile Çalıştırma

#### İlk Kez Çalıştırma
```bash
# Servisleri build edip başlatma
docker compose up --build

# Veya arka planda çalıştırmak için
docker compose up -d --build
```

#### Sonraki Çalıştırmalar
```bash
# Servisleri başlatma
docker compose up

# Veya arka planda çalıştırmak için
docker compose up -d
```

#### Servisleri Durdurma
```bash
# Servisleri durdurma
docker compose down
```

#### Logları Görüntüleme
```bash
# Tüm servislerin loglarını görüntüleme
docker compose logs -f

# Sadece backend loglarını görüntüleme
docker compose logs -f pdf-service

# Sadece frontend loglarını görüntüleme
docker compose logs -f web
```

### 3. Erişim
Servisler başlatıldıktan sonra aşağıdaki adreslere erişebilirsiniz:
- Frontend: http://localhost:5174
- Backend API: http://localhost:5001

## Kullanım

1. Web arayüzünde "PDF yüklemek için tıklayın" alanına tıklayın veya PDF dosyanızı sürükleyip bırakın
2. Filtre ayarlarını istediğiniz gibi düzenleyin:
   - Mürekkep Lekesi Yoğunluğu
   - Bulanıklık Seviyesi
   - Yazı Solukluğu
3. "Yükle ve İşle" butonuna tıklayın
4. İşlem tamamlandığında, işlenmiş PDF'i önizleyin ve indirin

## API Endpoint'leri

### PDF İşleme
- **URL**: `/process-pdf`
- **Metod**: `POST`
- **Content-Type**: `multipart/form-data`
- **Parametreler**:
  - `file`: PDF dosyası
  - `ink_spots`: Mürekkep lekesi yoğunluğu (0.99-0.9999)
  - `blur_radius`: Bulanıklık seviyesi (0-2)
  - `fade_level`: Yazı solukluğu (1-1.5)

## Geliştirme

### Yerel Geliştirme
1. Backend için:
```bash
cd backend
pip install -r requirements.txt
python app.py
```

2. Frontend için:
```bash
cd web
npm install
npm run dev
```

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın. 