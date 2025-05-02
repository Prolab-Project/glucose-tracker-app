from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base , Kullanici, Hasta_doktor, Olcum, Insulin# tüm sınıflar Baseye bagli
from datetime import datetime, date
from sqlalchemy import func


engine = create_engine("postgresql+psycopg2://postgres:1234@localhost/glucosedb")

Base.metadata.create_all(engine) #tablolar olsuturuyor zaten varsa atliyor.

Session= sessionmaker(bind=engine)
session = Session()

# Hastayı çek
hasta = session.query(Kullanici).filter_by(tc_kimlik_no="22222222222").first()

# Bugüne ait ölçümleri al (ortalama dahil olanlar)
bugun = date.today()

olcumler = session.query(Olcum).filter(
    Olcum.hasta_id == hasta.id,
    func.date(Olcum.tarih_saat) == bugun,
    Olcum.ortalamaya_dahil == True
).all()

# Ortalama hesapla
if olcumler:
    toplam = sum([o.kan_seker_degeri for o in olcumler])
    adet = len(olcumler)
    ortalama = toplam / adet
else:
    ortalama = None

# Doz belirle
doz = 0
if ortalama is not None:
    if ortalama < 70:
        doz = 0
    elif ortalama <= 110:
        doz = 0
    elif ortalama <= 150:
        doz = 1
    elif ortalama <= 200:
        doz = 2
    else:
        doz = 3

    # Kaydet
    insulin_kaydi = Insulin(
        hasta_id=hasta.id,
        tarih=bugun,
        ortalama_seker=ortalama,
        doz_miktari=doz
    )
    session.add(insulin_kaydi)
    session.commit()

    print(f"✅ Ortalama: {ortalama:.2f} mg/dL → Önerilen doz: {doz} ml")
else:
    print("⚠️ Bugüne ait ölçüm verisi bulunamadı.")