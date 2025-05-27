# Glikoz Takip Sistemi

Bu proje, diyabet hastalarının glikoz değerlerini takip etmek ve doktorların hastalarını yönetmek için geliştirilmiş kapsamlı bir sağlık yönetim sistemidir.

## 🎯 Özellikler

### Hasta Paneli
- Kişisel glikoz ölçümlerini kaydetme ve görüntüleme
- Ölçüm geçmişini analiz etme
- Doktor randevularını görüntüleme
- Kişisel bilgileri güncelleme
- Sağlık durumu raporlarını görüntüleme
- Egzersiz ve diyet takibi
- İnsülin kullanım kaydı
- Belirti takibi

### Doktor Paneli
- Hasta listesini görüntüleme ve yönetme
- Hasta glikoz değerlerini takip etme
- Hasta randevularını yönetme
- Hasta sağlık durumu raporlarını inceleme
- Hasta tedavi planlarını oluşturma ve güncelleme
- Hasta uyarılarını yönetme
- İnsülin doz takibi

## 🛠️ Teknolojiler

- Python 3.x
- PostgreSQL Veritabanı
- PyQt5 (Modern GUI arayüzü)
- Matplotlib (Veri görselleştirme)
- psycopg2 (PostgreSQL bağlantısı)

## 📋 Gereksinimler

```bash
pip install -r requirements.txt
```

## 🚀 Kurulum

1. PostgreSQL veritabanını kurun ve çalıştırın:
   - PostgreSQL'i [resmi sitesinden](https://www.postgresql.org/download/) indirin ve kurun
   - Veritabanı sunucusunu başlatın
   - `glucosedb` adında yeni bir veritabanı oluşturun:
   ```sql
   CREATE DATABASE glucosedb;
   ```

2. Veritabanı bağlantı bilgilerini ayarlayın:
   - `db_manager.py` ve `models.py` dosyalarında aşağıdaki bağlantı bilgilerini kendi ayarlarınıza göre güncelleyin:
   ```python
   dbname="glucosedb",
   user="postgres",
   password="1234",
   host="localhost"
   ```

3. Projeyi klonlayın:
```bash
git clone https://github.com/kullaniciadi/glucose-tracker-app.git
cd glucose-tracker-app
```

4. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

5. Veritabanı tablolarını oluşturun:
```bash
python models.py
```

6. Uygulamayı başlatın:
```bash
python login.py
```

## 🔐 Varsayılan Giriş Bilgileri

### Doktor Girişi
- TC No: 55555555555
- Şifre: doktor123

## 📁 Proje Yapısı

- `main.py` - Ana uygulama başlatıcı
- `login.py` - Giriş ekranı ve kimlik doğrulama
- `hasta_panel.py` - Hasta arayüzü ve işlevleri
- `doktor_panel.py` - Doktor arayüzü ve işlevleri
- `models.py` - Veritabanı şema tanımlamaları
- `db_manager.py` - Veritabanı yönetim işlemleri
- `styles.py` - Uygulama stil tanımlamaları
- `Data/` - Veritabanı yedekleri ve diğer veri dosyaları

## 📊 Veritabanı Şeması

Proje aşağıdaki tabloları içerir:
- `kullanici` - Kullanıcı bilgileri (hasta ve doktorlar)
- `hasta_doktor` - Hasta-doktor ilişkileri
- `olcum` - Glikoz ölçüm kayıtları
- `egzersiz` - Egzersiz takibi
- `diyet` - Diyet takibi
- `belirti` - Sağlık belirtileri
- `uyari` - Hasta uyarıları
- `insulin` - İnsülin kullanım kayıtları

## 🔒 Güvenlik

- Tüm şifreler SHA-256 ile hashlenerek saklanır
- Kullanıcı oturumları güvenli bir şekilde yönetilir
- Hassas sağlık verileri şifrelenerek saklanır
- PostgreSQL'in güvenlik özellikleri kullanılır

## 🤝 Katkıda Bulunma

1. Bu depoyu fork edin
2. Yeni bir özellik dalı oluşturun (`git checkout -b yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik: Açıklama'`)
4. Dalınıza push yapın (`git push origin yeni-ozellik`)
5. Bir Pull Request oluşturun

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 📞 İletişim

Proje Sahibi - [bedirhanereen@gmail.com]

Proje Linki: [https://github.com/bedirhaneren/glucose-tracker-app](https://github.com/kullaniciadi/glucose-tracker-app)
