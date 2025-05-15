from models import create_tables
from db_manager import DatabaseManager
from datetime import date, datetime
import hashlib
import sys

def main():
    print("Veritabanı tabloları kontrol ediliyor...")
    create_tables()
    
    print("Veritabanı tabloları başarıyla oluşturuldu.")
    
    db = DatabaseManager()
    
    db.cursor.execute("SELECT COUNT(*) FROM kullanici WHERE rol = 'doktor'")
    doktor_sayisi = db.cursor.fetchone()[0]
    
    if doktor_sayisi == 0:
        print("Veritabanında hiç doktor bulunmamaktadır.")
        print("İlk doktor kaydı oluşturuluyor...")
        
        tc_no = "55555555555"
        ad = "Ahmet"
        soyad = "Demir"
        dogum_tarihi = datetime.strptime("01.01.1980", "%d.%m.%Y").date()
        sifre = "doktor123"
        sifre_hash = hashlib.sha256(sifre.encode()).hexdigest()
        cinsiyet = "Kadın"
        eposta = "dr.ahmet@example.com"
        
        try:
            doktor_id = db.add_doctor(
                tc_no=tc_no,
                ad=ad,
                soyad=soyad,
                dogum_tarihi=dogum_tarihi,
                sifre_hash=sifre_hash,
                cinsiyet=cinsiyet,
                eposta=eposta
            )
            
            print(f"✅ Doktor kaydı başarıyla oluşturuldu:")
            print(f"   TC: {tc_no}")
            print(f"   Ad Soyad: {ad} {soyad}")
            print(f"   E-posta: {eposta}")
            print(f"   Şifre: {sifre}")
            print(f"   ID: {doktor_id}")
            print("\nBu bilgilerle sisteme giriş yapabilirsiniz.")
            
        except Exception as e:
            print(f"❌ Hata oluştu: {str(e)}")
    else:
        print(f"Veritabanında {doktor_sayisi} doktor bulunmaktadır. Yeni doktor kaydı eklenmedi.")
    
    print("\nProgram sonlandırılıyor...")

if __name__ == "__main__":
    main()