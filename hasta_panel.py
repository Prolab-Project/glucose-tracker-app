from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QListWidget, QPushButton, QLineEdit, QMessageBox, QComboBox, QFileDialog, QGraphicsPixmapItem, QHBoxLayout, QStackedWidget
from PyQt5.QtGui import QRegularExpressionValidator, QPixmap
from PyQt5.QtCore import QRegularExpression, Qt
from datetime import datetime
import hashlib
from styles import Styles

class BilgilerimPenceresi(QWidget):
    def __init__(self, hasta, db):
        super().__init__()
        self.hasta = hasta
        self.db = db
        
        self.layout = QVBoxLayout()
        
        self.profil_foto = QLabel()
        self.profil_foto.setFixedSize(150, 150)
        self.profil_foto.setStyleSheet("""
            QLabel {
                border: 2px solid #ccc;
                border-radius: 75px;
                background-color: #f0f0f0;
            }
        """)
        self.profil_foto.setScaledContents(True)
        
        self.bilgi_label = QLabel()
        self.bilgi_label.setStyleSheet("color: black; font-size: 16px;")
        
        self.guncelle_btn = QPushButton("✏️ Bilgileri Güncelle")
        self.guncelle_btn.setStyleSheet(Styles.get_button_style())
        
        self.layout.addWidget(self.profil_foto, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.bilgi_label)
        self.layout.addWidget(self.guncelle_btn)
        
        self.setLayout(self.layout)
        self.bilgileri_goster()
        
    def bilgileri_goster(self):
        if self.hasta['profil_resmi']:
            pixmap = QPixmap()
            pixmap.loadFromData(self.hasta['profil_resmi'])
            self.profil_foto.setPixmap(pixmap)
        else:
            self.profil_foto.setText("👤")
            self.profil_foto.setStyleSheet("""
                QLabel {
                    border: 2px solid #ccc;
                    border-radius: 75px;
                    background-color: #f0f0f0;
                    font-size: 72px;
                    qproperty-alignment: AlignCenter;
                }
            """)
            
        detay = (
            f"<b>Ad:</b> {self.hasta['ad']}<br>"
            f"<b>Soyad:</b> {self.hasta['soyad']}<br>"
            f"<b>TC:</b> {self.hasta['tc_kimlik_no']}<br>"
            f"<b>Email:</b> {self.hasta['eposta']}<br>"
            f"<b>Doğum Tarihi:</b> {self.hasta['dogum_tarihi'].strftime('%d.%m.%Y')}<br>"
            f"<b>Cinsiyet:</b> {self.hasta['cinsiyet']}<br>"
        )
        self.bilgi_label.setText(detay)

class HastaPanel(QWidget):    
    def __init__(self, hasta, hasta_id, db):
        super().__init__()

        self.setWindowTitle("Hasta paneli")
        self.setGeometry(100,100,800,600)
        self.hasta = hasta
        self.hasta_id = hasta_id
        self.db = db

        self.main_layout = QVBoxLayout()

        self.label = QLabel(f"Hoş geldiniz {hasta['ad']} {hasta['soyad']}")
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")

        button_layout = QHBoxLayout()
        self.bilgilerimButton = QPushButton("Bilgilerim", self)
        self.bilgilerimButton.setStyleSheet(Styles.get_button_style())
        self.olcumEkleButton = QPushButton("Yeni Ölçüm Ekle" , self)
        self.olcumEkleButton.setStyleSheet(Styles.get_button_style())
        
        button_layout.addWidget(self.bilgilerimButton)
        button_layout.addWidget(self.olcumEkleButton)

        self.main_layout.addWidget(self.label)
        self.main_layout.addLayout(button_layout)
        
        self.stacked_widget = QStackedWidget()
        
        self.bilgilerim_widget = BilgilerimPenceresi(self.hasta, self.db)
        self.stacked_widget.addWidget(self.bilgilerim_widget)
        
        self.main_layout.addWidget(self.stacked_widget)
        
        self.bilgilerimButton.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        
        self.setLayout(self.main_layout)

