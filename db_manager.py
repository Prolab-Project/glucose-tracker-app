import psycopg2
from datetime import datetime
import hashlib

class DatabaseManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="glucosedb",
            user="postgres",
            password="1234",
            host="localhost"
        )
        self.cursor = self.conn.cursor()
        
    def __del__(self):
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'conn'):
            self.conn.close()
            
    def commit(self):
        self.conn.commit()
        
    def rollback(self):
        self.conn.rollback()
        
    def get_user_by_tc(self, tc_no, sifre_hash=None):
        if sifre_hash is None:
            self.cursor.execute("""
                SELECT * FROM kullanici 
                WHERE tc_kimlik_no = %s
            """, (tc_no,))
        else:
            self.cursor.execute("""
                SELECT * FROM kullanici 
                WHERE tc_kimlik_no = %s AND sifre_hash = %s
            """, (tc_no, sifre_hash))
        return self.cursor.fetchone()
    
    def get_user_by_id(self, user_id):
        self.cursor.execute("""
            SELECT * FROM kullanici 
            WHERE id = %s
        """, (user_id,))
        return self.cursor.fetchone()
    
    def get_doctor_patients(self, doctor_id):
        self.cursor.execute("""
            SELECT k.* FROM kullanici k
            INNER JOIN hasta_doktor hd ON k.id = hd.hasta_id
            WHERE hd.doktor_id = %s
        """, (doctor_id,))
        return self.cursor.fetchall()
    
    def add_patient(self, tc_no, ad, soyad, dogum_tarihi, sifre_hash, cinsiyet, eposta, profil_resmi=None):
        try:
            self.cursor.execute("""
                INSERT INTO kullanici (tc_kimlik_no, ad, soyad, dogum_tarihi, sifre_hash, cinsiyet, rol, eposta, profil_resmi)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (tc_no, ad, soyad, dogum_tarihi, sifre_hash, cinsiyet, 'hasta', eposta, profil_resmi))
            hasta_id = self.cursor.fetchone()[0]
            self.commit()
            return hasta_id
        except Exception as e:
            self.rollback()
            raise e
    
    def add_patient_doctor_relation(self, doktor_id, hasta_id):
        try:
            self.cursor.execute("""
                INSERT INTO hasta_doktor (doktor_id, hasta_id)
                VALUES (%s, %s)
            """, (doktor_id, hasta_id))
            self.commit()
        except Exception as e:
            self.rollback()
            raise e
    
    def update_user(self, user_id, ad, soyad, eposta, cinsiyet, profil_resmi=None):
        try:
            if profil_resmi:
                self.cursor.execute("""
                    UPDATE kullanici 
                    SET ad = %s, soyad = %s, eposta = %s, cinsiyet = %s, profil_resmi = %s
                    WHERE id = %s
                """, (ad, soyad, eposta, cinsiyet, profil_resmi, user_id))
            else:
                self.cursor.execute("""
                    UPDATE kullanici 
                    SET ad = %s, soyad = %s, eposta = %s, cinsiyet = %s
                    WHERE id = %s
                """, (ad, soyad, eposta, cinsiyet, user_id))
            self.commit()
        except Exception as e:
            self.rollback()
            raise e
    
    def update_user_password(self, user_id, yeni_sifre_hash):
        try:
            self.cursor.execute("""
                UPDATE kullanici 
                SET sifre_hash = %s
                WHERE id = %s
            """, (yeni_sifre_hash, user_id))
            self.commit()
        except Exception as e:
            self.rollback()
            raise e
    
    def add_measurement(self, hasta_id, doktor_id, kan_seker_degeri, olcum_zamani):
        try:
            self.cursor.execute("""
                INSERT INTO olcum (hasta_id, doktor_id, tarih_saat, kan_seker_degeri, olcum_zamani, ortalamaya_dahil)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (hasta_id, doktor_id, datetime.now(), kan_seker_degeri, olcum_zamani, True))
            self.commit()
        except Exception as e:
            self.rollback()
            raise e
    
    def get_patient_measurements(self, hasta_id):
        self.cursor.execute("""
            SELECT * FROM olcum 
            WHERE hasta_id = %s 
            ORDER BY tarih_saat DESC
        """, (hasta_id,))
        return self.cursor.fetchall()
    
    def add_exercise(self, hasta_id, tarih, egzersiz_turu, egzersiz_durumu):
        try:
            self.cursor.execute("""
                INSERT INTO egzersiz (hasta_id, tarih, egzersiz_turu, egzersiz_durumu)
                VALUES (%s, %s, %s, %s)
            """, (hasta_id, tarih, egzersiz_turu, egzersiz_durumu))
            self.commit()
        except Exception as e:
            self.rollback()
            raise e
    
    def add_diet(self, hasta_id, tarih, diyet_turu, diyet_uygulandi):
        try:
            self.cursor.execute("""
                INSERT INTO diyet (hasta_id, tarih, diyet_turu, diyet_uygulandi)
                VALUES (%s, %s, %s, %s)
            """, (hasta_id, tarih, diyet_turu, diyet_uygulandi))
            self.commit()
        except Exception as e:
            self.rollback()
            raise e
    
    def add_symptom(self, hasta_id, tarih, belirti_turu):
        try:
            self.cursor.execute("""
                INSERT INTO belirti (hasta_id, tarih, belirti_turu)
                VALUES (%s, %s, %s)
            """, (hasta_id, tarih, belirti_turu))
            self.commit()
        except Exception as e:
            self.rollback()
            raise e
    
    def get_patient_exercises(self, hasta_id):
        self.cursor.execute("""
            SELECT * FROM egzersiz 
            WHERE hasta_id = %s 
            ORDER BY tarih DESC
        """, (hasta_id,))
        return self.cursor.fetchall()
    
    def get_patient_diets(self, hasta_id):
        self.cursor.execute("""
            SELECT * FROM diyet 
            WHERE hasta_id = %s 
            ORDER BY tarih DESC
        """, (hasta_id,))
        return self.cursor.fetchall()
    
    def get_patient_symptoms(self, hasta_id):
        self.cursor.execute("""
            SELECT * FROM belirti 
            WHERE hasta_id = %s 
            ORDER BY tarih DESC
        """, (hasta_id,))
        return self.cursor.fetchall()
    
    def get_patient_insulin(self, hasta_id, baslangic_tarih, bitis_tarih):
        self.cursor.execute("""
            SELECT * FROM insulin 
            WHERE hasta_id = %s 
            AND tarih BETWEEN %s AND %s
            ORDER BY tarih DESC
        """, (hasta_id, baslangic_tarih, bitis_tarih))
        return self.cursor.fetchall()
    
    def add_doctor(self, tc_no, ad, soyad, dogum_tarihi, sifre_hash, cinsiyet, eposta, profil_resmi=None):
        """Sisteme yeni bir doktor ekler"""
        try:
            self.cursor.execute("""
                INSERT INTO kullanici (tc_kimlik_no, ad, soyad, dogum_tarihi, sifre_hash, cinsiyet, rol, eposta, profil_resmi)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (tc_no, ad, soyad, dogum_tarihi, sifre_hash, cinsiyet, 'doktor', eposta, profil_resmi))
            doktor_id = self.cursor.fetchone()[0]
            self.commit()
            return doktor_id
        except Exception as e:
            self.rollback()
            raise e
    
    def add_insulin(self, hasta_id, tarih, ortalama_seker, doz_miktari):
        """Hastaya ait insülin önerisini kaydeder"""
        try:
            # Önce aynı hasta ve tarih için kayıt var mı kontrol et
            print(f"İnsülin kayıt kontrolü: Hasta ID={hasta_id}, Tarih={tarih}")
            self.cursor.execute("""
                SELECT id FROM insulin 
                WHERE hasta_id = %s AND tarih = %s
            """, (hasta_id, tarih))
            existing = self.cursor.fetchone()
            
            if existing:
                # Varsa güncelle
                print(f"Mevcut insülin kaydı güncelleniyor: ID={existing[0]}")
                self.cursor.execute("""
                    UPDATE insulin 
                    SET ortalama_seker = %s, doz_miktari = %s
                    WHERE hasta_id = %s AND tarih = %s
                """, (ortalama_seker, doz_miktari, hasta_id, tarih))
            else:
                # Yoksa yeni kayıt ekle
                print("Yeni insülin kaydı ekleniyor")
                self.cursor.execute("""
                    INSERT INTO insulin (hasta_id, tarih, ortalama_seker, doz_miktari)
                    VALUES (%s, %s, %s, %s)
                """, (hasta_id, tarih, ortalama_seker, doz_miktari))
            
            self.commit()
            print("İnsülin kayıt işlemi başarılı")
        except Exception as e:
            self.rollback()
            print(f"İnsülin kayıt hatası: {str(e)}")
            raise e
    
    def get_todays_insulin(self, hasta_id, tarih):
        """Belirli bir tarihteki insülin önerisini getirir"""
        print(f"İnsülin sorgusu: Hasta ID={hasta_id}, Tarih={tarih}")
        try:
            self.cursor.execute("""
                SELECT * FROM insulin 
                WHERE hasta_id = %s AND tarih = %s
            """, (hasta_id, tarih))
            result = self.cursor.fetchone()
            print(f"İnsülin sorgu sonucu: {result}")
            return result
        except Exception as e:
            print(f"İnsülin sorgu hatası: {str(e)}")
            return None 
        
    def add_alert(self, hasta_id, doktor_id , baslik , mesaj , tip , tarih)    : 
        try : 
            cursor= self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO uyarilar (hasta_id , doktor_id , baslik , mesaj , tip, tarih)
                VALUES(%s,%s,%s,%s,%s,%s)
                """,
            )
            self.conn.commit()
        except Exception as e:
            print(f"Uyarı kayıt hatası: {str(e)}")
            raise e
        
    def get_doctor_alerts (self, doktor_id) : 
        try : 
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT * FROM uyarilar WHERE doktor_id = %s
                ORDER BY tarih DESC
                """,
                (doktor_id,)
            )
            return cursor.fetchall()
        except Exception as e:
            print(f"Uyarı sorgu hatası: {str(e)}")
            return []
        
            
