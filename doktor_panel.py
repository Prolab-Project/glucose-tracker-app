from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QListWidget, QPushButton
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Kullanici, Hasta_doktor

engine = create_engine("postgresql+psycopg2://postgres:1234@localhost/glucosedb")
Session = sessionmaker(bind=engine)
session = Session()

class DoktorPanel(QWidget) : 
    def __init__(self, doktor):
        super().__init__()
        self.setWindowTitle("Doktor Paneli")     
        self.setGeometry(100,100,400,200)  
        self.doktor = doktor

        self.label = QLabel(f"Hoş geldiniz Dr. {doktor.ad} {doktor.soyad}")
        
        layout= QVBoxLayout()
    
        layout.addWidget(self.label)
        self.setLayout(layout) 



