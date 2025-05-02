from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base , Kullanici # tüm sınıflar Baseye bagli

engine = create_engine("postgresql+psycopg2://postgres:1234@localhost/glucosedb")

Base.metadata.create_all(engine) #tablolar olsuturuyor zaten varsa atliyor.
 
Session= sessionmaker(bind=engine)
session = Session()

doktor = Kullanici(
    tc_kimlik_no="11111111111",
    ad="Dr. Ayşe",
    soyad="Yılmaz",
    dogum_tarihi="1980-01-01",
    sifre_hash="hashlenmis1234",
    cinsiyet="Kadın",
    rol="doktor",
    eposta="ayse.doktor@example.com"
)

hasta = Kullanici(
    tc_kimlik_no="22222222222",
    ad="Ali",
    soyad="Kaya",
    dogum_tarihi="2002-05-10",
    sifre_hash="1234",  # sonra hash çevrilecek
    cinsiyet="Erkek",
    rol="hasta",
    eposta="ali.hasta@example.com"
)

session.add_all([doktor, hasta])
session.commit()
print("Test doktor ve hasta başarıyla eklendi.")

