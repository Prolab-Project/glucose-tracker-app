
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Kullanici
import sys

engine = create_engine("postgresql+psycopg2://postgres:1234@localhost/glucosedb")
Session = sessionmaker(bind=engine)
session = Session()

class LoginWindow(QWidget) : 
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login Screen")     
        self.setGeometry(100,100,400,200)

        layout = QVBoxLayout()

        self.tc_no = QLineEdit(self)
        self.tc_no.setPlaceholderText("TC kimlik no giriniz")
        self.sifre= QLineEdit (self)
        self.sifre.setPlaceholderText("Sifrenizi giriniz")         

        self.girisButton = QPushButton("Giris", self)
        self.girisButton.clicked.connect(self.on_button_click)

        layout.addWidget(self.tc_no)
        layout.addWidget(self.sifre) 
        layout.addWidget(self.girisButton)

        self.setLayout(layout)
        
    def on_button_click (self) : 
        tc_no = self.tc_no.text()
        sifre = self.sifre.text()
        kullanici = session.query(Kullanici ).filter_by(
            tc_kimlik_no=tc_no ,
            sifre_hash = sifre  
        ).first()
        
        if kullanici : 
            print("Giris basarili.")
            QMessageBox.information(self, "Basarili Giris", "Giris basarili ! Panele yonlendiriliyorsunuz.")
            
        else :
            print ("Hatali TC veya parola.")    
            QMessageBox.information(self, "Basarisiz Giris", " Hatali TC veya parola.")



app = QApplication(sys.argv) 
window = LoginWindow()
window.show()       

sys.exit(app.exec_())