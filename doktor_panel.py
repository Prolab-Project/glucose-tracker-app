from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QListWidget, QPushButton, QLineEdit,QMessageBox,QComboBox
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Kullanici, Hasta_doktor
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtCore import QRegularExpression
from datetime import datetime
import hashlib

class HastaListePenceresi(QWidget) :    
    def __init__(self, doktor_id, session):
        super().__init__()

        self.setWindowTitle("Hastalarım")    
        self.setGeometry(100,100,400,200)
        self.doktor = doktor_id
        self.session = session
        self.hasta_listesi = QListWidget()

        layoutHastaListe= QVBoxLayout()
        layoutHastaListe.addWidget(self.hasta_listesi)
        self.setLayout(layoutHastaListe)
        self.hastalari_getir()

        self.hasta_listesi.itemDoubleClicked.connect(self.hasta_detaylarini_goster)
    
    def hasta_detaylarini_goster(self, item):
        tc = item.text().split("TC: ")[-1]
        hasta = self.session.query(Kullanici).filter_by(tc_kimlik_no=tc).first()

        if hasta:
            detay = f"Ad: {hasta.ad}\nSoyad: {hasta.soyad}\nTC: {hasta.tc_kimlik_no}\nEmail: {hasta.eposta}\nDoğum Tarihi: {hasta.dogum_tarihi}"
            detay_penceresi = QWidget()
            detay_penceresi.setWindowTitle("Hasta Detayı")
            detay_penceresi.setGeometry(200, 200, 300, 200)
            layout = QVBoxLayout()
            layout.addWidget(QLabel(detay))

            detay_penceresi.setLayout(layout)
            detay_penceresi.show()

            self.detay_penceresi = detay_penceresi


    def hastalari_getir(self) : 
        print("sadasd")
        eslesmeler= self.session.query(Hasta_doktor).filter_by(doktor_id=self.doktor.id).all()
        for eslesme in eslesmeler: 
            hasta = self.session.query(Kullanici).filter_by(id=eslesme.hasta_id).first()
            self.hasta_listesi.addItem(f"{hasta.ad} {hasta.soyad} - TC: {hasta.tc_kimlik_no}")

class HastaEklePenceresi(QWidget): 
    def __init__(self, doktor_id, session):
        super().__init__()
        self.setWindowTitle("Hasta Ekle")
        self.setGeometry(100,100,400,200)         
        self.doktor =doktor_id
        self.session = session

        self.tc_no_label = QLabel("TC Kimlik NO")
        self.tc_no= QLineEdit(self)
        self.tc_no.setPlaceholderText("Hasta TC Kimlik NO")

        self.tc_no.setMaxLength(11)
        regex = QRegularExpression("^[0-9]{0,11}$")
        self.tc_no.setValidator(QRegularExpressionValidator(regex))

        self.ad_label = QLabel ("Hasta Adı") 
        self.ad = QLineEdit(self)
        self.ad.setPlaceholderText("Hasta adını giriniz.") 

        self.soyad_label = QLabel("Hasta Soyadı") 
        self.soyad = QLineEdit(self)
        self.soyad.setPlaceholderText("Hasta soyadını giriniz") 

        self.cinsiyet_label = QLabel("Hasta Cinsiyeti")
        self.cinsiyet= QComboBox()
        self.cinsiyet.addItems(["Erkek","Kadın"]) #baska cinsiyet yoktur

        self.dogum_tarihi_label = QLabel("Hasta Doğum Tarihi") 
        self.dogum_tarihi = QLineEdit(self)
        self.dogum_tarihi.setPlaceholderText("Hasta doğum tarihini giriniz. ")

        self.eposta_label= QLabel("Hasta E-posta adresi")
        self.eposta= QLineEdit(self)
        self.eposta.setPlaceholderText("Hasta epostası giriniz") 

        self.sifre_label = QLabel("Hasta Sifre")
        self.sifre = QLineEdit(self)
        self.sifre.setPlaceholderText("Hasta Sifresini giriniz")

        self.sifre_tekrar_label = QLabel("Hasta Sifre (Tekrar)")
        self.sifre_tekrar = QLineEdit(self)
        self.sifre_tekrar.setPlaceholderText("Hasta sifresini tekrar giriniz")

        self.kayit_button = QPushButton("Kayıt Oluştur",self)
        self.kayit_button.clicked.connect(self.HastaKayitOlustur)

        layout = QVBoxLayout()
        layout.addWidget(self.tc_no_label)
        layout.addWidget(self.tc_no)
        layout.addWidget(self.ad_label)
        layout.addWidget(self.ad)
        layout.addWidget(self.soyad_label)
        layout.addWidget(self.soyad)
        layout.addWidget(self.cinsiyet_label)
        layout.addWidget(self.cinsiyet)
        layout.addWidget(self.dogum_tarihi_label)
        layout.addWidget(self.dogum_tarihi)
        layout.addWidget(self.eposta_label)
        layout.addWidget(self.eposta)
        layout.addWidget(self.sifre_label)
        layout.addWidget(self.sifre)
        layout.addWidget(self.sifre_tekrar_label)
        layout.addWidget(self.sifre_tekrar)
        layout.addWidget(self.kayit_button)
        self.setLayout(layout)

    def HastaKayitOlustur(self): 
        tc=self.tc_no.text()
        ad= self.ad.text()
        soyad = self.soyad.text()
        dogum_tarihi = self.dogum_tarihi.text()
        eposta= self.eposta.text()
        sifre = self.sifre.text()
        sifre_tekrar =self.sifre_tekrar.text()
        cinsiyet = self.cinsiyet.currentText()

        if not all([tc, ad, soyad, dogum_tarihi, eposta, sifre, sifre_tekrar,cinsiyet, ]):
            QMessageBox.warning(self, "Eksik Bilgi", "Lütfen tüm alanları doldurun.")
            return        
        if sifre != sifre_tekrar  : 
            QMessageBox.warning(self, "Şifreler Eşleşmiyor", "Girdiğiniz şifreler eşleşmiyor. Lütfen kontrol ediniz.")
            return
        mevcut = self.session.query(Kullanici).filter_by(tc_kimlik_no=tc).first()
        if mevcut : 
            QMessageBox.warning(self, "Zaten var", "Bu TC'ye sahip hasta zaten sisteme kayıtlı.")
            return
        
        try:
            dogum_tarihi = datetime.strptime(dogum_tarihi, "%d.%m.%Y").date()
        except ValueError:
            QMessageBox.warning(self, "Hatalı Tarih", "Doğum tarihi DD.MM.YYYY formatında olmalı.")
            return        

        sifre_hash = hashlib.sha256(sifre.encode()).hexdigest()
        yeni_hasta= Kullanici  (
            tc_kimlik_no = tc,
            ad=ad, 
            soyad= soyad,
            dogum_tarihi = dogum_tarihi,
            sifre_hash= sifre_hash,
            eposta=eposta,
            cinsiyet=cinsiyet,
            rol= 'hasta',
            profil_resmi = None
        )
        self.session.add(yeni_hasta)
        self.session.commit()

        eslesme = Hasta_doktor(
            doktor_id= self.doktor.id,
            hasta_id = yeni_hasta.id
        )
        self.session.add(eslesme)
        self.session.commit()
        
        QMessageBox.information(self, "Başarılı", "Yeni hasta kaydınız başarıyla yapılmıştır.")
        self.close()

    
                    
class DoktorPanel(QWidget) : 
    def __init__(self, doktor,doktor_id, session):
            super().__init__()
            self.setWindowTitle("Doktor Paneli")     
            self.setGeometry(100,100,400,200)  
            self.doktor = doktor
            self.doktor_id =doktor_id
            self.session = session

            self.label = QLabel(f"Hoş geldiniz Dr. {doktor.ad} {doktor.soyad}")
            self.hasta_listesi = QListWidget()
            self.hastaGoruntule = QPushButton("Hastalarımı Görüntüle ",self)
            self.hastaGoruntule.clicked.connect(self.hasta_penceresini_ac)

            self.hastaEkleButton = QPushButton("Yeni Hasta Kaydı",self)
            self.hastaEkleButton.clicked.connect(self.hasta_ekle_penceresini_ac)

            layout= QVBoxLayout()
            layout.addWidget(self.hastaGoruntule)
            layout.addWidget(self.label)
            layout.addWidget(self.hasta_listesi)
            layout.addWidget(self.hastaEkleButton)
            self.setLayout(layout) 

    def hasta_penceresini_ac(self)   : 
           self.hasta_penceresi = HastaListePenceresi(self.doktor, self.session)
           self.hasta_penceresi.show()
    def hasta_ekle_penceresini_ac(self) : 
            self.hasta_ekle_penceresi = HastaEklePenceresi(self.doktor, self.session)   
            self.hasta_ekle_penceresi.show()    
           

