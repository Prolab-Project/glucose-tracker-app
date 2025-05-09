from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QRegularExpressionValidator, QPixmap, QFont
from PyQt5.QtCore import QRegularExpression, Qt
import sys
from doktor_panel import DoktorPanel
import hashlib
from hasta_panel import HastaPanel
from db_manager import DatabaseManager

db = DatabaseManager()

class LoginWindow(QWidget): 
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Diyabet Takip Uygulaması")     
        self.setGeometry(100,100,800,600)
        self.showMaximized()
        
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
            }
            QLabel {
                color: #ffffff;
            }
        """)

        main_layout = QHBoxLayout()
        
        left_layout = QVBoxLayout()
        left_widget = QWidget()
        left_widget.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                border-radius: 20px;
            }
        """)
        
        logo_label = QLabel("🩺")
        logo_label.setStyleSheet("""
            QLabel {
                font-size: 120px;
                color: #3498db;
            }
        """)
        logo_label.setAlignment(Qt.AlignCenter)
        
        title_label = QLabel("Diyabet Takip\nUygulaması")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 36px;
                font-weight: bold;
                color: #ffffff;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        
        subtitle_label = QLabel("Sağlığınız bizimle güvende")
        subtitle_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #bdc3c7;
            }
        """)
        subtitle_label.setAlignment(Qt.AlignCenter)
        
        left_layout.addStretch()
        left_layout.addWidget(logo_label)
        left_layout.addWidget(title_label)
        left_layout.addWidget(subtitle_label)
        left_layout.addStretch()
        
        left_widget.setLayout(left_layout)
        left_widget.setFixedWidth(400)
        
        right_layout = QVBoxLayout()
        right_widget = QWidget()
        right_widget.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                border-radius: 20px;
            }
        """)
        
        form_layout = QVBoxLayout()
        form_layout.setSpacing(20)
        
        welcome_label = QLabel("Hoş Geldiniz")
        welcome_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: bold;
                color: #ffffff;
                margin-bottom: 20px;
            }
        """)
        welcome_label.setAlignment(Qt.AlignCenter)
        
        self.tc_label = QLabel("TC Kimlik Numarası")
        self.tc_label.setStyleSheet("font-size: 14px; color: #bdc3c7;")
        self.tc_no = QLineEdit(self)
        self.tc_no.setPlaceholderText("TC kimlik no giriniz")
        self.tc_no.setMaxLength(11)
        regex = QRegularExpression("^[0-9]{0,11}$")
        self.tc_no.setValidator(QRegularExpressionValidator(regex))
        self.tc_no.setStyleSheet(self.get_input_style())

        self.sifre_label = QLabel("Şifre")
        self.sifre_label.setStyleSheet("font-size: 14px; color: #bdc3c7;")
        self.sifre = QLineEdit(self)
        self.sifre.setPlaceholderText("Şifrenizi giriniz")
        self.sifre.setStyleSheet(self.get_input_style())
        self.sifre.setEchoMode(QLineEdit.Password)
        
        self.girisButton = QPushButton("Giriş Yap", self)
        self.girisButton.setStyleSheet(self.get_button_style())
        self.girisButton.clicked.connect(self.giris_button_clicked)
        
        form_layout.addWidget(welcome_label)
        form_layout.addWidget(self.tc_label)
        form_layout.addWidget(self.tc_no)
        form_layout.addWidget(self.sifre_label)
        form_layout.addWidget(self.sifre)
        form_layout.addWidget(self.girisButton)
        form_layout.addStretch()
        
        right_widget.setLayout(form_layout)
        
        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)
        
        self.setLayout(main_layout)
    
    def get_input_style(self):
        return """
        QLineEdit {
            padding: 15px;
            border: 2px solid #34495e;
            border-radius: 10px;
            font-size: 16px;
            background-color: #34495e;
            color: #ffffff;
        }
        QLineEdit:focus {
            border-color: #3498db;
            background-color: #2c3e50;
        }
        QLineEdit::placeholder {
            color: #95a5a6;
        }
        """

    def get_button_style(self):
        return """
        QPushButton {
            padding: 15px;
            font-size: 16px;
            font-weight: bold;
            background-color: #3498db;
            color: white;
            border-radius: 10px;
            border: none;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
        QPushButton:pressed {
            background-color: #2471a3;
        }
        """        
    def giris_button_clicked(self): 
        tc_no = self.tc_no.text()
        sifre = self.sifre.text()
        sifre_hash = hashlib.sha256(sifre.encode()).hexdigest()
        
        kullanici = db.get_user_by_tc(tc_no, sifre_hash)
        
        if kullanici: 
            print("Giris basarili.")
            QMessageBox.information(self, "Başarılı Giriş", "Giriş başarılı! Panele yönlendiriliyorsunuz.")
            
            kullanici_dict = {
                'id': kullanici[0],
                'tc_kimlik_no': kullanici[1],
                'ad': kullanici[2],
                'soyad': kullanici[3],
                'dogum_tarihi': kullanici[4],
                'sifre_hash': kullanici[5],
                'cinsiyet': kullanici[6],
                'rol': kullanici[7],
                'eposta': kullanici[8],
                'profil_resmi': kullanici[9]
            }
            
            if kullanici_dict['rol'] == 'doktor': 
                self.hide()
                self.doktor_panel = DoktorPanel(kullanici_dict, kullanici_dict['id'], db)
                self.doktor_panel.show()
            elif kullanici_dict['rol'] == 'hasta': 
                self.hide()
                self.hasta_panel = HastaPanel(kullanici_dict, kullanici_dict['id'], db)
                self.hasta_panel.show() 
        else:
            print("Hatali TC veya parola.")    
            QMessageBox.warning(self, "Başarısız Giriş", "Hatalı TC veya parola.")

app = QApplication(sys.argv) 
window = LoginWindow()
window.show()       
sys.exit(app.exec_())