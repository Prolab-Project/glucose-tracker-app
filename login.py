
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Kullanici
import sys
from doktor_panel import DoktorPanel

engine = create_engine("postgresql+psycopg2://postgres:1234@localhost/glucosedb")
Session = sessionmaker(bind=engine)
session = Session()

class LoginWindow(QWidget) : 
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login Screen")     
        self.setGeometry(100,100,400,200)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f4f8;
                font-family: Arial;
                font-size: 14px;
            }
            QLabel {
                font-weight: bold;
                color: #333;
                margin-top: 10px;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #aaa;
                border-radius: 5px;
                background-color: #fff;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)


        layout = QVBoxLayout()
        
        self.tc_label = QLabel("TC Kimlik Numarası")
        self.tc_no = QLineEdit(self)
        self.tc_no.setPlaceholderText("TC kimlik no giriniz")
        self.sifre_label = QLabel("Şifre")
        self.sifre= QLineEdit (self)
        self.sifre.setPlaceholderText("Sifrenizi giriniz") 
        self.sifre.setEchoMode(QLineEdit.Password) # *** seklinde gorulmesi icin
        
        self.girisButton = QPushButton("Giris", self)
        self.girisButton.clicked.connect(self.giris_button_clicked)

        layout.addWidget(self.tc_label)
        layout.addWidget(self.tc_no)
        layout.addWidget(self.sifre_label)
        layout.addWidget(self.sifre) 
        layout.addWidget(self.girisButton)
        
        self.setLayout(layout)
        
    def giris_button_clicked (self) : 
        tc_no = self.tc_no.text()
        sifre = self.sifre.text()
        kullanici = session.query(Kullanici ).filter_by(
            tc_kimlik_no=tc_no ,
            sifre_hash = sifre  
        ).first()
        
        if kullanici : 
            print("Giris basarili.")
            QMessageBox.information(self, "Basarili Giris", "Giris basarili ! Panele yonlendiriliyorsunuz.")
            if (kullanici.rol == 'doktor') : 
                self.hide()
                self.doktor_panel = DoktorPanel(kullanici)
                self.doktor_panel.show()
          #  if (kullanici.rol == 'hasta' ): 
           #     self.hide()
           #     self.hasta_panel = HastaPanel(kullanici)
            #    self.hasta_panel.show() 
        else :
            print ("Hatali TC veya parola.")    
            QMessageBox.information(self, "Basarisiz Giris", " Hatali TC veya parola.")



app = QApplication(sys.argv) 
window = LoginWindow()
window.show()       

sys.exit(app.exec_())