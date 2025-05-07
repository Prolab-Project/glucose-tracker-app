import psycopg2
from datetime import datetime

def create_tables():
    conn = psycopg2.connect(
        dbname="glucosedb",
        user="postgres",
        password="1234",
        host="localhost"
    )
    cursor = conn.cursor()
    
    try:
        # Kullanıcı tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS kullanici (
                id SERIAL PRIMARY KEY,
                tc_kimlik_no VARCHAR(11) UNIQUE NOT NULL,
                ad VARCHAR(50) NOT NULL,
                soyad VARCHAR(50) NOT NULL,
                dogum_tarihi DATE,
                sifre_hash TEXT NOT NULL,
                cinsiyet VARCHAR(10),
                rol VARCHAR(10) NOT NULL,
                eposta VARCHAR(100) UNIQUE,
                profil_resmi BYTEA
            )
        """)
        
        # Hasta-Doktor ilişki tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hasta_doktor (
                id SERIAL PRIMARY KEY,
                hasta_id INTEGER REFERENCES kullanici(id) ON DELETE CASCADE,
                doktor_id INTEGER REFERENCES kullanici(id) ON DELETE CASCADE
            )
        """)
        
        # Ölçüm tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS olcum (
                id SERIAL PRIMARY KEY,
                hasta_id INTEGER REFERENCES kullanici(id) ON DELETE CASCADE,
                doktor_id INTEGER REFERENCES kullanici(id) ON DELETE CASCADE,
                tarih_saat TIMESTAMP NOT NULL,
                kan_seker_degeri INTEGER NOT NULL,
                olcum_zamani VARCHAR(15),
                ortalamaya_dahil BOOLEAN DEFAULT TRUE
            )
        """)
        
        # Egzersiz tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS egzersiz (
                id SERIAL PRIMARY KEY,
                hasta_id INTEGER REFERENCES kullanici(id) ON DELETE CASCADE,
                tarih DATE NOT NULL,
                egzersiz_turu VARCHAR(30),
                egzersiz_durumu BOOLEAN DEFAULT FALSE
            )
        """)
        
        # Diyet tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS diyet (
                id SERIAL PRIMARY KEY,
                hasta_id INTEGER REFERENCES kullanici(id) ON DELETE CASCADE,
                tarih DATE NOT NULL,
                diyet_turu VARCHAR(30),
                diyet_uygulandi BOOLEAN DEFAULT FALSE
            )
        """)
        
        # Belirti tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS belirti (
                id SERIAL PRIMARY KEY,
                hasta_id INTEGER REFERENCES kullanici(id) ON DELETE CASCADE,
                tarih DATE NOT NULL,
                belirti_turu VARCHAR(30)
            )
        """)
        
        # Uyarı tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS uyari (
                id SERIAL PRIMARY KEY,
                hasta_id INTEGER REFERENCES kullanici(id) ON DELETE CASCADE,
                tarih_saat TIMESTAMP NOT NULL,
                uyari_turu VARCHAR(50),
                mesaj TEXT
            )
        """)
        
        # İnsülin tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS insulin (
                id SERIAL PRIMARY KEY,
                hasta_id INTEGER REFERENCES kullanici(id) ON DELETE CASCADE,
                tarih DATE NOT NULL,
                ortalama_seker FLOAT,
                doz_miktari FLOAT
            )
        """)
        
        conn.commit()
        print("Veritabanı tabloları başarıyla oluşturuldu.")
        
    except Exception as e:
        conn.rollback()
        print(f"Hata oluştu: {str(e)}")
        
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_tables()


