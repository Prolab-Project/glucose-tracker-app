from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QListWidget, QPushButton, QLineEdit, QMessageBox, QComboBox, QFileDialog, QGraphicsPixmapItem, QHBoxLayout, QStackedWidget, QDateEdit, QTimeEdit, QSpinBox
from PyQt5.QtGui import QRegularExpressionValidator, QPixmap
from PyQt5.QtCore import QRegularExpression, Qt, QDate, QTime
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

class EgzersizTakipPenceresi(QWidget):
    def __init__(self, hasta, db):
        super().__init__()
        self.hasta = hasta
        self.db = db
        
        layout = QVBoxLayout()
        
        baslik = QLabel("🏃 Egzersiz Takibi")
        baslik.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        
        self.egzersiz_turu = QComboBox()
        self.egzersiz_turu.addItems(["Yürüyüş", "Bisiklet", "Klinik Egzersiz"])
        self.egzersiz_turu.setStyleSheet(Styles.get_input_style())
        
        self.tarih = QDateEdit()
        self.tarih.setDate(QDate.currentDate())
        self.tarih.setStyleSheet(Styles.get_input_style())
        
        self.durum = QComboBox()
        self.durum.addItems(["Yapıldı", "Yapılmadı"])
        self.durum.setStyleSheet(Styles.get_input_style())
        
        self.kaydet_btn = QPushButton("Egzersiz Durumunu Kaydet")
        self.kaydet_btn.setStyleSheet(Styles.get_button_style())
        self.kaydet_btn.clicked.connect(self.egzersiz_kaydet)
        
        layout.addWidget(baslik)
        layout.addWidget(QLabel("Egzersiz Türü:"))
        layout.addWidget(self.egzersiz_turu)
        layout.addWidget(QLabel("Tarih:"))
        layout.addWidget(self.tarih)
        layout.addWidget(QLabel("Durum:"))
        layout.addWidget(self.durum)
        layout.addWidget(self.kaydet_btn)
        
        self.setLayout(layout)
    
    def egzersiz_kaydet(self):
        try:
            self.db.add_exercise(
                self.hasta['id'],
                self.tarih.date().toPyDate(),
                self.egzersiz_turu.currentText(),
                self.durum.currentText() == "Yapıldı"
            )
            QMessageBox.information(self, "Başarılı", "Egzersiz durumu kaydedildi.")
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Egzersiz kaydedilirken bir hata oluştu: {str(e)}")

class DiyetTakipPenceresi(QWidget):
    def __init__(self, hasta, db):
        super().__init__()
        self.hasta = hasta
        self.db = db
        
        layout = QVBoxLayout()
        
        baslik = QLabel("🍽️ Diyet Takibi")
        baslik.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        
        self.diyet_turu = QComboBox()
        self.diyet_turu.addItems(["Az Şekerli Diyet", "Şekersiz Diyet", "Dengeli Beslenme"])
        self.diyet_turu.setStyleSheet(Styles.get_input_style())
        
        self.tarih = QDateEdit()
        self.tarih.setDate(QDate.currentDate())
        self.tarih.setStyleSheet(Styles.get_input_style())
        
        self.durum = QComboBox()
        self.durum.addItems(["Uygulandı", "Uygulanmadı"])
        self.durum.setStyleSheet(Styles.get_input_style())
        
        self.kaydet_btn = QPushButton("Diyet Durumunu Kaydet")
        self.kaydet_btn.setStyleSheet(Styles.get_button_style())
        self.kaydet_btn.clicked.connect(self.diyet_kaydet)
        
        layout.addWidget(baslik)
        layout.addWidget(QLabel("Diyet Türü:"))
        layout.addWidget(self.diyet_turu)
        layout.addWidget(QLabel("Tarih:"))
        layout.addWidget(self.tarih)
        layout.addWidget(QLabel("Durum:"))
        layout.addWidget(self.durum)
        layout.addWidget(self.kaydet_btn)
        
        self.setLayout(layout)
    
    def diyet_kaydet(self):
        try:
            self.db.add_diet(
                self.hasta['id'],
                self.tarih.date().toPyDate(),
                self.diyet_turu.currentText(),
                self.durum.currentText() == "Uygulandı"
            )
            QMessageBox.information(self, "Başarılı", "Diyet durumu kaydedildi.")
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Diyet kaydedilirken bir hata oluştu: {str(e)}")

class BelirtiTakipPenceresi(QWidget):
    def __init__(self, hasta, db):
        super().__init__()
        self.hasta = hasta
        self.db = db
        
        layout = QVBoxLayout()
        
        baslik = QLabel("⚠️ Belirti Takibi")
        baslik.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        
        self.belirti_turu = QComboBox()
        self.belirti_turu.addItems([
            "Poliüri (Sık idrara çıkma)",
            "Polifaji (Aşırı açlık hissi)",
            "Polidipsi (Aşırı susama hissi)",
            "Nöropati (El ve ayaklarda karıncalanma veya uyuşma hissi)",
            "Kilo kaybı",
            "Yorgunluk",
            "Yaraların yavaş iyileşmesi",
            "Bulanık görme"
        ])
        self.belirti_turu.setStyleSheet(Styles.get_input_style())
        
        self.tarih = QDateEdit()
        self.tarih.setDate(QDate.currentDate())
        self.tarih.setStyleSheet(Styles.get_input_style())
        
        self.kaydet_btn = QPushButton("Belirtiyi Kaydet")
        self.kaydet_btn.setStyleSheet(Styles.get_button_style())
        self.kaydet_btn.clicked.connect(self.belirti_kaydet)
        
        layout.addWidget(baslik)
        layout.addWidget(QLabel("Belirti Türü:"))
        layout.addWidget(self.belirti_turu)
        layout.addWidget(QLabel("Tarih:"))
        layout.addWidget(self.tarih)
        layout.addWidget(self.kaydet_btn)
        
        self.setLayout(layout)
    
    def belirti_kaydet(self):
        try:
            self.db.add_symptom(
                self.hasta['id'],
                self.tarih.date().toPyDate(),
                self.belirti_turu.currentText()
            )
            QMessageBox.information(self, "Başarılı", "Belirti kaydedildi.")
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Belirti kaydedilirken bir hata oluştu: {str(e)}")

class KanSekeriOlcumPenceresi(QWidget):
    def __init__(self, hasta, db):
        super().__init__()
        self.hasta = hasta
        self.db = db
        
        layout = QVBoxLayout()
        
        baslik = QLabel("🩸 Kan Şekeri Ölçümü")
        baslik.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        
        self.kan_sekeri = QSpinBox()
        self.kan_sekeri.setRange(0, 1000)
        self.kan_sekeri.setStyleSheet(Styles.get_input_style())
        
        self.olcum_zamani = QComboBox()
        self.olcum_zamani.addItems(["Sabah", "Öğle", "Akşam", "Gece"])
        self.olcum_zamani.setStyleSheet(Styles.get_input_style())
        
        self.tarih = QDateEdit()
        self.tarih.setDate(QDate.currentDate())
        self.tarih.setStyleSheet(Styles.get_input_style())
        
        self.saat = QTimeEdit()
        self.saat.setTime(QTime.currentTime())
        self.saat.setStyleSheet(Styles.get_input_style())
        
        self.kaydet_btn = QPushButton("Ölçümü Kaydet")
        self.kaydet_btn.setStyleSheet(Styles.get_button_style())
        self.kaydet_btn.clicked.connect(self.olcum_kaydet)
        
        layout.addWidget(baslik)
        layout.addWidget(QLabel("Kan Şekeri Değeri (mg/dL):"))
        layout.addWidget(self.kan_sekeri)
        layout.addWidget(QLabel("Ölçüm Zamanı:"))
        layout.addWidget(self.olcum_zamani)
        layout.addWidget(QLabel("Tarih:"))
        layout.addWidget(self.tarih)
        layout.addWidget(QLabel("Saat:"))
        layout.addWidget(self.saat)
        layout.addWidget(self.kaydet_btn)
        
        self.setLayout(layout)
    
    def olcum_kaydet(self):
        try:
            tarih_saat = datetime.combine(
                self.tarih.date().toPyDate(),
                self.saat.time().toPyTime()
            )
            self.db.add_measurement(
                self.hasta['id'],
                None,  # doktor_id None olarak bırakılıyor çünkü hasta kendisi giriyor
                self.kan_sekeri.value(),
                self.olcum_zamani.currentText()
            )
            QMessageBox.information(self, "Başarılı", "Kan şekeri ölçümü kaydedildi.")
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Ölçüm kaydedilirken bir hata oluştu: {str(e)}")

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
        self.egzersizButton = QPushButton("Egzersiz Takibi", self)
        self.egzersizButton.setStyleSheet(Styles.get_button_style())
        self.diyetButton = QPushButton("Diyet Takibi", self)
        self.diyetButton.setStyleSheet(Styles.get_button_style())
        self.belirtiButton = QPushButton("Belirti Takibi", self)
        self.belirtiButton.setStyleSheet(Styles.get_button_style())
        
        button_layout.addWidget(self.bilgilerimButton)
        button_layout.addWidget(self.olcumEkleButton)
        button_layout.addWidget(self.egzersizButton)
        button_layout.addWidget(self.diyetButton)
        button_layout.addWidget(self.belirtiButton)

        self.main_layout.addWidget(self.label)
        self.main_layout.addLayout(button_layout)
        
        self.stacked_widget = QStackedWidget()
        
        self.bilgilerim_widget = BilgilerimPenceresi(self.hasta, self.db)
        self.olcum_widget = KanSekeriOlcumPenceresi(self.hasta, self.db)
        self.egzersiz_widget = EgzersizTakipPenceresi(self.hasta, self.db)
        self.diyet_widget = DiyetTakipPenceresi(self.hasta, self.db)
        self.belirti_widget = BelirtiTakipPenceresi(self.hasta, self.db)
        
        self.stacked_widget.addWidget(self.bilgilerim_widget)
        self.stacked_widget.addWidget(self.olcum_widget)
        self.stacked_widget.addWidget(self.egzersiz_widget)
        self.stacked_widget.addWidget(self.diyet_widget)
        self.stacked_widget.addWidget(self.belirti_widget)
        
        self.main_layout.addWidget(self.stacked_widget)
        
        self.bilgilerimButton.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.olcumEkleButton.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.egzersizButton.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.diyetButton.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.belirtiButton.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        
        self.setLayout(self.main_layout)

