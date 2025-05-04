
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Kullanici
import sys
from doktor_panel import DoktorPanel
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtCore import QRegularExpression

engine = create_engine("postgresql+psycopg2://postgres:1234@localhost/glucosedb")
Session = sessionmaker(bind=engine)
session = Session()

class LoginWindow(QWidget) : 
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login Screen")     
        self.setGeometry(100,100,400,200)
        self.showMaximized()
        
        self.setStyleSheet("""
            QWidget {
                background-image: url('arkaplan.jpg');
                background-repeat: no-repeat;
                background-position: center;
            }
        """)

        layout = QVBoxLayout()
        
        self.tc_label = QLabel("TC Kimlik Numarası")
        self.tc_no = QLineEdit(self)
        self.tc_no.setPlaceholderText("TC kimlik no giriniz")
        self.tc_no.setMaxLength(11)
        regex = QRegularExpression("^[0-9]{0,11}$")
        self.tc_no.setValidator(QRegularExpressionValidator(regex))
        self.tc_no.setStyleSheet(self.get_input_style())

        self.sifre_label = QLabel("Şifre")
        self.sifre= QLineEdit (self)
        self.sifre.setPlaceholderText("Sifrenizi giriniz")
        self.sifre.setStyleSheet(self.get_input_style())
        self.sifre.setEchoMode(QLineEdit.Password) # *** seklinde gorulmesi icin
        
        self.girisButton = QPushButton("Giris", self)
        self.girisButton.setStyleSheet(self.get_button_style())
        self.girisButton.clicked.connect(self.giris_button_clicked)

        layout.addWidget(self.tc_label)
        layout.addWidget(self.tc_no)
        layout.addWidget(self.sifre_label)
        layout.addWidget(self.sifre) 
        layout.addWidget(self.girisButton)
        
        self.setLayout(layout)
    
    def get_input_style(self):
        return """
        QLineEdit {
            padding: 12px;
            border: 2px solid #2980b9;
            border-radius: 10px;
            font-size: 16px;
            background-color: #fdfefe;
        }
        QLineEdit:focus {
            border-color: #1abc9c;
        }
        """

    def get_button_style(self):
        return """
        QPushButton {
            padding: 10px;
            font-size: 16px;
            background-color: #2980b9;
            color: white;
            border-radius: 10px;
        }
        QPushButton:hover {
            background-color: #1abc9c;
        }
        """        
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
                self.doktor_panel = DoktorPanel(kullanici, kullanici.id,session)
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