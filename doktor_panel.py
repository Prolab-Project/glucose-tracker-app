from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QListWidget, QPushButton, QLineEdit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Kullanici, Hasta_doktor
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtCore import QRegularExpression

engine = create_engine("postgresql+psycopg2://postgres:1234@localhost/glucosedb")
Session = sessionmaker(bind=engine)
session = Session()

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
        eslesmeler= session.query(Hasta_doktor).filter_by(doktor_id=self.doktor.id).all()
        for eslesme in eslesmeler: 
            hasta = session.query(Kullanici).filter_by(id=eslesme.hasta_id).first()
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

        self.dogum_tarihi_label = QLabel("Hasta Doğum Tarihi") 
        self.dogum_tarihi = QLineEdit(self)
        self.dogum_tarihi.setPlaceholderText("Hasta doğum tarihini giriniz. ")

        self.eposta_label= QLabel("Hasta E-posta adresi")
        self.eposta= QLineEdit(self)
        self.eposta.setPlaceholderText("Hasta epostası giriniz") 

        self.sifre_label = QLabel("Hasta Sifre")
        self.sifre = QLineEdit(self)
        self.sifre.setPlaceholderText("Hasta Sifresini giriniz")

        self.kayit_button = QPushButton("Kayıt Oluştur",self)


        layout = QVBoxLayout()
        layout.addWidget(self.tc_no_label)
        layout.addWidget(self.tc_no)
        layout.addWidget(self.ad_label)
        layout.addWidget(self.ad)
        layout.addWidget(self.soyad_label)
        layout.addWidget(self.soyad)
        layout.addWidget(self.dogum_tarihi_label)
        layout.addWidget(self.dogum_tarihi)
        layout.addWidget(self.eposta_label)
        layout.addWidget(self.eposta)
        layout.addWidget(self.sifre_label)
        layout.addWidget(self.sifre)
        layout.addWidget(self.kayit_button)
        self.setLayout(layout)
    
                    
class DoktorPanel(QWidget) : 
    def __init__(self, doktor):
            super().__init__()
            self.setWindowTitle("Doktor Paneli")     
            self.setGeometry(100,100,400,200)  
            self.doktor = doktor

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
           self.hasta_penceresi = HastaListePenceresi(self.doktor, session)
           self.hasta_penceresi.show()
    def hasta_ekle_penceresini_ac(self) : 
            self.hasta_ekle_penceresi = HastaEklePenceresi(self.doktor, session)   
            self.hasta_ekle_penceresi.show()    
           

