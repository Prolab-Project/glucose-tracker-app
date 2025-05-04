from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QListWidget, QPushButton
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Kullanici, Hasta_doktor

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


    def hastalari_getir(self) : 
        print("sadasd")
        eslesmeler= session.query(Hasta_doktor).filter_by(doktor_id=self.doktor.id).all()
        for eslesme in eslesmeler: 
            hasta = session.query(Kullanici).filter_by(id=eslesme.hasta_id).first()
            self.hasta_listesi.addItem(f"{hasta.ad} {hasta.soyad} - TC: {hasta.tc_kimlik_no}")

                    
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

            layout= QVBoxLayout()
            layout.addWidget(self.hastaGoruntule)
            layout.addWidget(self.label)
            layout.addWidget(self.hasta_listesi)
            self.setLayout(layout) 

    def hasta_penceresini_ac(self)   : 
           self.hasta_penceresi = HastaListePenceresi(self.doktor, session)
           self.hasta_penceresi.show()
           

