from sqlalchemy import Column, Integer, String, Date, Text, LargeBinary, Boolean, Float, ForeignKey, TIMESTAMP
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Kullanici (Base) : 
    __tablename__ = 'kullanici' 
    id = Column(Integer, primary_key=True)
    tc_kimlik_no = Column(String(11), unique=True, nullable= False )
    ad = Column(String(50), nullable=False) 
    soyad= Column(String(50), nullable=False)
    dogum_tarihi = Column(Date)
    sifre_hash = Column(Text, nullable=False)
    cinsiyet= Column(String(10))
    rol = Column(String(10), nullable=False)
    eposta = Column(String(100), unique=True)
    profil_resmi = Column(LargeBinary)

class Hasta_doktor(Base) : 
    __tablename__ = 'hasta_doktor'
    id = Column(Integer, primary_key=True)
    hasta_id = Column(Integer,ForeignKey(Kullanici.id, ondelete='CASCADE')) #referance kullanici_id
    doktor_id = Column(Integer, ForeignKey (Kullanici.id, ondelete='CASCADE'))

class Olcum(Base) : 
    __tablename__ = 'olcum'
    id = Column(Integer, primary_key=True)
    hasta_id = Column(Integer,ForeignKey(Kullanici.id, ondelete='CASCADE')) #referance kullanici_id
    doktor_id = Column(Integer, ForeignKey (Kullanici.id, ondelete='CASCADE'))
    tarih_saat= Column(TIMESTAMP ,nullable= False) 
    kan_seker_degeri = Column (Integer, nullable=False) 
    olcum_zamani = Column (String(15))
    ortalamaya_dahil = Column (Boolean, default= True )

class Egzersiz(Base) : 
    __tablename__ = 'egzersiz'
    id = Column(Integer, primary_key=True)
    hasta_id = Column(Integer,ForeignKey(Kullanici.id, ondelete='CASCADE')) #referance kullanici_id
    tarih= Column(Date, nullable= False)
    egzersiz_turu = Column (String(30))
    egzersiz_durumu = Column (Boolean , default=False)

class Diyet(Base) : 
    __tablename__ = 'diyet'
    id = Column(Integer, primary_key=True)
    hasta_id = Column(Integer,ForeignKey(Kullanici.id, ondelete='CASCADE')) #referance kullanici_id
    tarih= Column(Date, nullable= False)
    diyet_turu = Column (String(30))
    diyet_uygulandi = Column (Boolean , default=False)

class Belirti(Base) : 
    __tablename__ = 'belirti'
    id = Column(Integer, primary_key=True)
    hasta_id = Column(Integer,ForeignKey(Kullanici.id, ondelete='CASCADE')) #referance kullanici_id
    tarih= Column(Date, nullable= False)
    belirti_turu = Column (String(30))


class Uyari(Base): 
    __tablename__ ='uyari' 
    id = Column(Integer, primary_key=True)
    hasta_id = Column(Integer,ForeignKey(Kullanici.id, ondelete='CASCADE')) #referance kullanici_id
    tarih_saat= Column(TIMESTAMP, nullable= False)
    uyari_turu = Column (String(50))
    mesaj= Column(Text)



class Insulin(Base): 
    __tablename__ ='insulin' 
    id = Column(Integer, primary_key=True)
    hasta_id = Column(Integer,ForeignKey(Kullanici.id, ondelete='CASCADE')) #referance kullanici_id
    tarih= Column(Date, nullable= False)
    ortalama_seker  = Column (Float)
    doz_miktari = Column (Float)
  


