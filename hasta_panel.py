from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QListWidget, QPushButton, QLineEdit, QMessageBox, QComboBox, QFileDialog, QGraphicsPixmapItem, QHBoxLayout, QStackedWidget
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Kullanici, Hasta_doktor, Olcum
from PyQt5.QtGui import QRegularExpressionValidator, QPixmap
from PyQt5.QtCore import QRegularExpression, Qt
from datetime import datetime
import hashlib
from PyQt5.QtGui import QPixmap

class HastaPanel(QWidget) :    
    def __init__(self, hasta,hasta_id, session):
        super().__init__()

        self.setWindowTitle("Hasta paneli")
        self.setGeometry(100,100,400,200)
        self.hasta = hasta
        self.hasta_id = hasta_id
        self.session = session 

        self.main_layout =QVBoxLayout()

        self.label = QLabel(f"Hoş geldiniz {hasta.ad} {hasta.soyad}")
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")

        button_layout = QHBoxLayout()
        self.bilgilerimButton = QPushButton("Bilgilerim", self)
        self.bilgilerimButton.setStyleSheet(self.get_button_style())

        self.olcumEkleButton = QPushButton("Yeni Ölçüm Ekle" , self)
        self.olcumEkleButton.setStyleSheet(self.get_button_style())
        
        button_layout.addWidget(self.bilgilerimButton)
        button_layout.addWidget(self.olcumEkleButton)

        self.main_layout.addWidget(self.label)
        self.main_layout.addLayout(button_layout)
        
        self.setLayout(self.main_layout)

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