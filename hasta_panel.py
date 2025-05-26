from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QListWidget, QPushButton, QLineEdit, QMessageBox, QComboBox, QFileDialog, QGraphicsPixmapItem, QHBoxLayout, QStackedWidget, QDateEdit, QTimeEdit, QSpinBox, QProgressBar, QFrame, QScrollArea
from PyQt5.QtGui import QRegularExpressionValidator, QPixmap
from PyQt5.QtCore import QRegularExpression, Qt, QDate, QTime
from datetime import datetime, timedelta
import hashlib
from styles import Styles
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class BilgilerimPenceresi(QWidget):
    def __init__(self, hasta, db):
        super().__init__()
        self.hasta = hasta
        self.db = db
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Scroll Area oluştur
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 0px 0px 0px 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #3498db;
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        # İçerik için konteyner widget oluştur
        content_widget = QWidget()
        self.layout = QVBoxLayout(content_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)
        
        # Ana kart frame
        self.main_frame = QFrame()
        self.main_frame.setStyleSheet(Styles.get_modern_card_style())
        main_layout_frame = QVBoxLayout(self.main_frame)
        main_layout_frame.setContentsMargins(25, 25, 25, 25)
        main_layout_frame.setSpacing(15)
        
        # Başlık
        baslik = QLabel("👤 Kişisel Bilgilerim")
        baslik.setStyleSheet(Styles.get_title_style())
        main_layout_frame.addWidget(baslik, alignment=Qt.AlignCenter)
        
        # Profil bölümü
        profil_frame = QFrame()
        profil_frame.setStyleSheet(Styles.get_inner_card_style())
        profil_layout = QVBoxLayout(profil_frame)
        
        self.profil_foto = QLabel()
        self.profil_foto.setFixedSize(150, 150)
        self.profil_foto.setStyleSheet(Styles.get_modern_profile_image_style())
        self.profil_foto.setScaledContents(True)
        
        self.resim_degistir_btn = QPushButton("🖼️ Profil Resmi Değiştir")
        self.resim_degistir_btn.setStyleSheet(Styles.get_modern_button_style())
        self.resim_degistir_btn.clicked.connect(self.profil_resmi_degistir)
        
        profil_layout.addWidget(self.profil_foto, alignment=Qt.AlignCenter)
        profil_layout.addWidget(self.resim_degistir_btn, alignment=Qt.AlignCenter)
        
        # Bilgi kartı
        bilgi_frame = QFrame()
        bilgi_frame.setStyleSheet(Styles.get_inner_card_style())
        bilgi_layout = QVBoxLayout(bilgi_frame)
        
        bilgi_baslik = QLabel("Kişisel Bilgiler")
        bilgi_baslik.setStyleSheet(Styles.get_subtitle_style())
        
        self.bilgi_label = QLabel()
        self.bilgi_label.setStyleSheet(Styles.get_label_style("#34495e", 16))
        
        bilgi_layout.addWidget(bilgi_baslik)
        bilgi_layout.addWidget(self.bilgi_label)
        
        # Şifre değiştirme kartı
        self.sifre_frame = QFrame()
        self.sifre_frame.setStyleSheet(Styles.get_inner_card_style())
        sifre_layout = QVBoxLayout(self.sifre_frame)
        
        sifre_baslik = QLabel("🔒 Şifre Değiştir")
        sifre_baslik.setStyleSheet(Styles.get_subtitle_style())
        
        self.eski_sifre = QLineEdit()
        self.eski_sifre.setPlaceholderText("Mevcut Şifre")
        self.eski_sifre.setEchoMode(QLineEdit.Password)
        self.eski_sifre.setStyleSheet(Styles.get_modern_input_style())
        
        self.yeni_sifre = QLineEdit()
        self.yeni_sifre.setPlaceholderText("Yeni Şifre")
        self.yeni_sifre.setEchoMode(QLineEdit.Password)
        self.yeni_sifre.setStyleSheet(Styles.get_modern_input_style())
        
        self.yeni_sifre_tekrar = QLineEdit()
        self.yeni_sifre_tekrar.setPlaceholderText("Yeni Şifre (Tekrar)")
        self.yeni_sifre_tekrar.setEchoMode(QLineEdit.Password)
        self.yeni_sifre_tekrar.setStyleSheet(Styles.get_modern_input_style())
        
        self.sifre_degistir_btn = QPushButton("Şifreyi Değiştir")
        self.sifre_degistir_btn.setStyleSheet(Styles.get_modern_button_style())
        self.sifre_degistir_btn.clicked.connect(self.sifre_degistir)
        
        sifre_layout.addWidget(sifre_baslik)
        sifre_layout.addWidget(self.eski_sifre)
        sifre_layout.addWidget(self.yeni_sifre)
        sifre_layout.addWidget(self.yeni_sifre_tekrar)
        sifre_layout.addWidget(self.sifre_degistir_btn)
        
        # Ana düzene ekle
        main_layout_frame.addWidget(profil_frame)
        main_layout_frame.addWidget(bilgi_frame)
        main_layout_frame.addWidget(self.sifre_frame)
        
        self.layout.addWidget(self.main_frame)
        
        scroll_area.setWidget(content_widget)
        
        main_layout.addWidget(scroll_area)
        
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
                    border: 3px solid #3498db;
                    border-radius: 75px;
                    background-color: #f0f0f0;
                    font-size: 72px;
                    qproperty-alignment: AlignCenter;
                }
            """)
            
        detay = (
            f"<table style='width: 100%; border-spacing: 10px;'>"
            f"<tr><td style='font-weight: bold; color: #3498db;'>Ad:</td><td>{self.hasta['ad']}</td></tr>"
            f"<tr><td style='font-weight: bold; color: #3498db;'>Soyad:</td><td>{self.hasta['soyad']}</td></tr>"
            f"<tr><td style='font-weight: bold; color: #3498db;'>TC:</td><td>{self.hasta['tc_kimlik_no']}</td></tr>"
            f"<tr><td style='font-weight: bold; color: #3498db;'>Email:</td><td>{self.hasta['eposta']}</td></tr>"
            f"<tr><td style='font-weight: bold; color: #3498db;'>Doğum Tarihi:</td><td>{self.hasta['dogum_tarihi'].strftime('%d.%m.%Y')}</td></tr>"
            f"<tr><td style='font-weight: bold; color: #3498db;'>Cinsiyet:</td><td>{self.hasta['cinsiyet']}</td></tr>"
            f"</table>"
        )
        self.bilgi_label.setText(detay)
    
    def profil_resmi_degistir(self):
        dosya_yolu, _ = QFileDialog.getOpenFileName(
            self,
            "Profil Resmi Seç",
            "",
            "Resim Dosyaları (*.png *.jpg *.jpeg)"
        )
        
        if dosya_yolu:
            try:
                with open(dosya_yolu, 'rb') as f:
                    resim_data = f.read()
                
                self.db.update_user(
                    self.hasta['id'],
                    self.hasta['ad'],
                    self.hasta['soyad'],
                    self.hasta['eposta'],
                    self.hasta['cinsiyet'],
                    resim_data
                )
                
                self.hasta['profil_resmi'] = resim_data
                self.bilgileri_goster()
                QMessageBox.information(self, "Başarılı", "Profil resmi başarıyla güncellendi.")
                
            except Exception as e:
                QMessageBox.warning(self, "Hata", f"Profil resmi güncellenirken bir hata oluştu: {str(e)}")
    
    def sifre_degistir(self):
        eski_sifre = self.eski_sifre.text()
        yeni_sifre = self.yeni_sifre.text()
        yeni_sifre_tekrar = self.yeni_sifre_tekrar.text()
        
        if not eski_sifre or not yeni_sifre or not yeni_sifre_tekrar:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun.")
            return
        
        if yeni_sifre != yeni_sifre_tekrar:
            QMessageBox.warning(self, "Hata", "Yeni şifreler eşleşmiyor.")
            return
        
        try:
            eski_sifre_hash = hashlib.sha256(eski_sifre.encode()).hexdigest()
            yeni_sifre_hash = hashlib.sha256(yeni_sifre.encode()).hexdigest()
            
            if eski_sifre_hash != self.hasta['sifre_hash']:
                QMessageBox.warning(self, "Hata", "Mevcut şifre yanlış.")
                return
            
            self.db.update_user_password(self.hasta['id'], yeni_sifre_hash)
            self.hasta['sifre_hash'] = yeni_sifre_hash
            
            self.eski_sifre.clear()
            self.yeni_sifre.clear()
            self.yeni_sifre_tekrar.clear()
            
            QMessageBox.information(self, "Başarılı", "Şifreniz başarıyla güncellendi.")
            
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Şifre güncellenirken bir hata oluştu: {str(e)}")

class EgzersizTakipPenceresi(QWidget):
    def __init__(self, hasta, db, dashboard=None):
        super().__init__()
        self.hasta = hasta
        self.db = db
        self.dashboard = dashboard
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 0px 0px 0px 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #3498db;
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)
        
        main_card = QFrame()
        main_card.setStyleSheet(Styles.get_modern_card_style())
        card_layout = QVBoxLayout(main_card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(20)
        
        baslik = QLabel("🏃 Egzersiz Takibi")
        baslik.setStyleSheet(Styles.get_title_style())
        card_layout.addWidget(baslik, alignment=Qt.AlignCenter)
        
        bilgi_label = QLabel("Düzenli egzersiz, kan şekeri seviyenizi kontrol etmenize yardımcı olur.")
        bilgi_label.setStyleSheet("font-size: 14px; color: #7f8c8d; margin-bottom: 15px;")
        bilgi_label.setWordWrap(True)
        card_layout.addWidget(bilgi_label)
        
        tur_frame = QFrame()
        tur_frame.setStyleSheet(Styles.get_inner_card_style())
        tur_layout = QVBoxLayout(tur_frame)
        
        tur_baslik = QLabel("🚲 Egzersiz Türü")
        tur_baslik.setStyleSheet(Styles.get_subtitle_style())
        tur_layout.addWidget(tur_baslik)
        
        self.egzersiz_turu = QComboBox()
        self.egzersiz_turu.addItems(["Yürüyüş", "Bisiklet", "Koşu", "Yüzme", "Pilates", "Yoga", "Klinik Egzersiz", "Diğer"])
        self.egzersiz_turu.setStyleSheet(Styles.get_modern_combobox_style())
        tur_layout.addWidget(self.egzersiz_turu)
        
        tarih_frame = QFrame()
        tarih_frame.setStyleSheet(Styles.get_inner_card_style())
        tarih_layout = QVBoxLayout(tarih_frame)
        
        tarih_baslik = QLabel("📅 Tarih")
        tarih_baslik.setStyleSheet(Styles.get_subtitle_style())
        tarih_layout.addWidget(tarih_baslik)
        
        self.tarih = QDateEdit()
        self.tarih.setDate(QDate.currentDate())
        self.tarih.setCalendarPopup(True)
        self.tarih.setStyleSheet(Styles.get_modern_dateedit_style())
        tarih_layout.addWidget(self.tarih)
        
        durum_frame = QFrame()
        durum_frame.setStyleSheet(Styles.get_inner_card_style())
        durum_layout = QVBoxLayout(durum_frame)
        
        durum_baslik = QLabel("✅ Durum")
        durum_baslik.setStyleSheet(Styles.get_subtitle_style())
        durum_layout.addWidget(durum_baslik)
        
        self.durum = QComboBox()
        self.durum.addItems(["Yapıldı", "Yapılmadı"])
        self.durum.setStyleSheet(Styles.get_modern_combobox_style())
        durum_layout.addWidget(self.durum)
        
        kaydet_frame = QFrame()
        kaydet_frame.setStyleSheet(Styles.get_inner_card_style())
        kaydet_layout = QVBoxLayout(kaydet_frame)
        
        kaydet_bilgi = QLabel("Egzersiz kaydınızı oluşturun ve sağlıklı kalın!")
        kaydet_bilgi.setStyleSheet("font-size: 13px; color: #7f8c8d; font-style: italic; margin-bottom: 10px;")
        kaydet_layout.addWidget(kaydet_bilgi)
        
        self.kaydet_btn = QPushButton("💾 Egzersiz Durumunu Kaydet")
        self.kaydet_btn.setStyleSheet(Styles.get_success_button_style())
        self.kaydet_btn.clicked.connect(self.egzersiz_kaydet)
        kaydet_layout.addWidget(self.kaydet_btn)
        
        card_layout.addWidget(tur_frame)
        card_layout.addWidget(tarih_frame)
        card_layout.addWidget(durum_frame)
        card_layout.addWidget(kaydet_frame)
        
        content_layout.addWidget(main_card)
        
        scroll_area.setWidget(content_widget)
        
        main_layout.addWidget(scroll_area)
    
    def egzersiz_kaydet(self):
        try:
            self.db.add_exercise(
                self.hasta['id'],
                self.tarih.date().toPyDate(),
                self.egzersiz_turu.currentText(),
                self.durum.currentText() == "Yapıldı"
            )
            QMessageBox.information(self, "Başarılı", "Egzersiz durumu kaydedildi.")
            if self.dashboard:
                self.dashboard.verileri_guncelle()
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Egzersiz kaydedilirken bir hata oluştu: {str(e)}")

class DiyetTakipPenceresi(QWidget):
    def __init__(self, hasta, db, dashboard=None):
        super().__init__()
        self.hasta = hasta
        self.db = db
        self.dashboard = dashboard
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 0px 0px 0px 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #3498db;
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)
        
        main_card = QFrame()
        main_card.setStyleSheet(Styles.get_modern_card_style())
        card_layout = QVBoxLayout(main_card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(20)
        
        baslik = QLabel("🍽️ Diyet Takibi")
        baslik.setStyleSheet(Styles.get_title_style())
        card_layout.addWidget(baslik, alignment=Qt.AlignCenter)
        
        bilgi_label = QLabel("Doğru beslenme, kan şekeri kontrolünde en önemli adımlardan biridir.")
        bilgi_label.setStyleSheet("font-size: 14px; color: #7f8c8d; margin-bottom: 15px;")
        bilgi_label.setWordWrap(True)
        card_layout.addWidget(bilgi_label)
        
        diyet_frame = QFrame()
        diyet_frame.setStyleSheet(Styles.get_inner_card_style())
        diyet_layout = QVBoxLayout(diyet_frame)
        
        diyet_baslik = QLabel("🥗 Diyet Türü")
        diyet_baslik.setStyleSheet(Styles.get_subtitle_style())
        diyet_layout.addWidget(diyet_baslik)
        
        self.diyet_turu = QComboBox()
        self.diyet_turu.addItems(["Az Şekerli Diyet", "Şekersiz Diyet", "Düşük Karbonhidratlı Diyet", "Akdeniz Diyeti", "Dengeli Beslenme", "Ketojenik Diyet"])
        self.diyet_turu.setStyleSheet(Styles.get_modern_combobox_style())
        diyet_layout.addWidget(self.diyet_turu)
        
        tarih_frame = QFrame()
        tarih_frame.setStyleSheet(Styles.get_inner_card_style())
        tarih_layout = QVBoxLayout(tarih_frame)
        
        tarih_baslik = QLabel("📅 Tarih")
        tarih_baslik.setStyleSheet(Styles.get_subtitle_style())
        tarih_layout.addWidget(tarih_baslik)
        
        self.tarih = QDateEdit()
        self.tarih.setDate(QDate.currentDate())
        self.tarih.setCalendarPopup(True)
        self.tarih.setStyleSheet(Styles.get_modern_dateedit_style())
        tarih_layout.addWidget(self.tarih)
        
        durum_frame = QFrame()
        durum_frame.setStyleSheet(Styles.get_inner_card_style())
        durum_layout = QVBoxLayout(durum_frame)
        
        durum_baslik = QLabel("✅ Durum")
        durum_baslik.setStyleSheet(Styles.get_subtitle_style())
        durum_layout.addWidget(durum_baslik)
        
        self.durum = QComboBox()
        self.durum.addItems(["Uygulandı", "Uygulanmadı"])
        self.durum.setStyleSheet(Styles.get_modern_combobox_style())
        durum_layout.addWidget(self.durum)
        
        kaydet_frame = QFrame()
        kaydet_frame.setStyleSheet(Styles.get_inner_card_style())
        kaydet_layout = QVBoxLayout(kaydet_frame)
        
        kaydet_bilgi = QLabel("Diyet uygulamanız sağlıklı bir yaşam için önemlidir.")
        kaydet_bilgi.setStyleSheet("font-size: 13px; color: #7f8c8d; font-style: italic; margin-bottom: 10px;")
        kaydet_layout.addWidget(kaydet_bilgi)
        
        self.kaydet_btn = QPushButton("💾 Diyet Durumunu Kaydet")
        self.kaydet_btn.setStyleSheet(Styles.get_success_button_style())
        self.kaydet_btn.clicked.connect(self.diyet_kaydet)
        kaydet_layout.addWidget(self.kaydet_btn)
        
        card_layout.addWidget(diyet_frame)
        card_layout.addWidget(tarih_frame)
        card_layout.addWidget(durum_frame)
        card_layout.addWidget(kaydet_frame)
        
        content_layout.addWidget(main_card)
        
        scroll_area.setWidget(content_widget)
        
        main_layout.addWidget(scroll_area)
    
    def diyet_kaydet(self):
        try:
            self.db.add_diet(
                self.hasta['id'],
                self.tarih.date().toPyDate(),
                self.diyet_turu.currentText(),
                self.durum.currentText() == "Uygulandı"
            )
            QMessageBox.information(self, "Başarılı", "Diyet durumu kaydedildi.")
            if self.dashboard:
                self.dashboard.verileri_guncelle()
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Diyet kaydedilirken bir hata oluştu: {str(e)}")

class BelirtiTakipPenceresi(QWidget):
    def __init__(self, hasta, db):
        super().__init__()
        self.hasta = hasta
        self.db = db
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 0px 0px 0px 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #3498db;
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)
        
        main_card = QFrame()
        main_card.setStyleSheet(Styles.get_modern_card_style())
        card_layout = QVBoxLayout(main_card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(20)
        
        baslik = QLabel("⚠️ Belirti Takibi")
        baslik.setStyleSheet(Styles.get_title_style())
        card_layout.addWidget(baslik, alignment=Qt.AlignCenter)
        
        bilgi_label = QLabel("Belirtilerinizi takip etmek, sağlık durumunuzu izlemek için önemlidir.")
        bilgi_label.setStyleSheet("font-size: 14px; color: #7f8c8d; margin-bottom: 15px;")
        bilgi_label.setWordWrap(True)
        card_layout.addWidget(bilgi_label)
        
        belirti_frame = QFrame()
        belirti_frame.setStyleSheet(Styles.get_inner_card_style())
        belirti_layout = QVBoxLayout(belirti_frame)
        
        belirti_baslik = QLabel("🔍 Belirti Türü")
        belirti_baslik.setStyleSheet(Styles.get_subtitle_style())
        belirti_layout.addWidget(belirti_baslik)
        
        self.belirti_turu = QComboBox()
        self.belirti_turu.addItems([
            "Poliüri (Sık idrara çıkma)",
            "Polifaji (Aşırı açlık hissi)",
            "Polidipsi (Aşırı susama hissi)",
            "Nöropati (El ve ayaklarda karıncalanma veya uyuşma hissi)",
            "Kilo kaybı",
            "Yorgunluk",
            "Yaraların yavaş iyileşmesi",
            "Bulanık görme",
            "Baş dönmesi",
            "Halsizlik",
            "Cilt kuruluğu"
        ])
        self.belirti_turu.setStyleSheet(Styles.get_modern_combobox_style())
        belirti_layout.addWidget(self.belirti_turu)
        
        tarih_frame = QFrame()
        tarih_frame.setStyleSheet(Styles.get_inner_card_style())
        tarih_layout = QVBoxLayout(tarih_frame)
        
        tarih_baslik = QLabel("📅 Tarih")
        tarih_baslik.setStyleSheet(Styles.get_subtitle_style())
        tarih_layout.addWidget(tarih_baslik)
        
        self.tarih = QDateEdit()
        self.tarih.setDate(QDate.currentDate())
        self.tarih.setCalendarPopup(True)
        self.tarih.setStyleSheet(Styles.get_modern_dateedit_style())
        tarih_layout.addWidget(self.tarih)
        
        kaydet_frame = QFrame()
        kaydet_frame.setStyleSheet(Styles.get_inner_card_style())
        kaydet_layout = QVBoxLayout(kaydet_frame)
        
        kaydet_bilgi = QLabel("Belirtilerinizi düzenli olarak kaydedin ve doktorunuzla paylaşın.")
        kaydet_bilgi.setStyleSheet("font-size: 13px; color: #7f8c8d; font-style: italic; margin-bottom: 10px;")
        kaydet_layout.addWidget(kaydet_bilgi)
        
        self.kaydet_btn = QPushButton("💾 Belirtiyi Kaydet")
        self.kaydet_btn.setStyleSheet(Styles.get_success_button_style())
        self.kaydet_btn.clicked.connect(self.belirti_kaydet)
        kaydet_layout.addWidget(self.kaydet_btn)
        
        card_layout.addWidget(belirti_frame)
        card_layout.addWidget(tarih_frame)
        card_layout.addWidget(kaydet_frame)
        
        content_layout.addWidget(main_card)
        
        scroll_area.setWidget(content_widget)
        
        main_layout.addWidget(scroll_area)
    
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

class GrafikPenceresi(QWidget):
    def __init__(self, hasta, db):
        super().__init__()
        self.hasta = hasta
        self.db = db
        self.setWindowTitle("Kan Şekeri Grafiği")
        self.setGeometry(200, 200, 800, 600)
        
        layout = QVBoxLayout()
        
        # Matplotlib figürü oluştur
        self.figure = Figure(figsize=(10, 6), facecolor='#2c3e50')
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor('#34495e')
        self.figure.patch.set_facecolor('#2c3e50')
        
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
        self.grafigi_guncelle()
    
    def grafigi_guncelle(self):
        bugun = datetime.now().date()
        olcumler = self.db.get_patient_measurements(self.hasta['id'])
        bugun_olcumler = [o for o in olcumler if o[3].date() == bugun]
        
        # Ölçüm zamanlarının sırası
        zaman_sirasi = {"Sabah": 0, "Öğle": 1, "İkindi": 2, "Akşam": 3, "Gece": 4}
        
        self.ax.clear()
        if bugun_olcumler:
            # Ölçümleri zamana göre sırala
            bugun_olcumler.sort(key=lambda x: zaman_sirasi[x[5]])  # x[5] olcum_zamani
            
            olcum_zamanlari = [o[5] for o in bugun_olcumler]  # olcum_zamani
            degerler = [o[4] for o in bugun_olcumler]  # olcum_degeri
            
            # Grafik çizgisini çiz
            self.ax.plot(olcum_zamanlari, degerler, 'o-', color='#3498db', linewidth=2, markersize=8)
            
            # Her noktanın üzerine değeri yaz
            for i, (zaman, deger) in enumerate(zip(olcum_zamanlari, degerler)):
                self.ax.annotate(f'{deger}', 
                               (zaman, deger), 
                               textcoords="offset points", 
                               xytext=(0,10), 
                               ha='center',
                               color='white',
                               fontsize=10)
            
            # Grafik ayarları
            self.ax.set_xlabel('Ölçüm Zamanı', color='white', fontsize=12)
            self.ax.set_ylabel('Kan Şekeri (mg/dL)', color='white', fontsize=12)
            self.ax.tick_params(axis='x', colors='white', rotation=45)
            self.ax.tick_params(axis='y', colors='white')
            self.ax.grid(True, color='#95a5a6', alpha=0.2)
            
            # Hedef aralığını göster
            self.ax.axhspan(70, 180, color='#27ae60', alpha=0.1, label='Hedef Aralık')
            self.ax.legend(loc='upper right', facecolor='#2c3e50', labelcolor='white')
            
            # Grafik başlığı
            self.ax.set_title('Günlük Kan Şekeri Takibi', color='white', pad=20, fontsize=14)
            
            # Grafik kenarlarını ayarla
            self.ax.spines['bottom'].set_color('white')
            self.ax.spines['top'].set_color('white')
            self.ax.spines['left'].set_color('white')
            self.ax.spines['right'].set_color('white')
        else:
            self.ax.text(0.5, 0.5, 'Bugün için ölçüm bulunmamaktadır.',
                        horizontalalignment='center',
                        verticalalignment='center',
                        transform=self.ax.transAxes,
                        color='white',
                        fontsize=12)
            self.ax.set_xticks([])
            self.ax.set_yticks([])
        
        # Grafiği yenile
        self.figure.tight_layout()
        self.canvas.draw()

class KanSekeriOlcumPenceresi(QWidget):
    def __init__(self, hasta, db, dashboard=None):
        super().__init__()
        self.hasta = hasta
        self.db = db
        self.dashboard = dashboard
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 0px 0px 0px 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #3498db;
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        # İçerik widget'ı oluştur
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)
        
        # Ana kart frame
        self.main_card = QFrame()
        self.main_card.setStyleSheet(Styles.get_modern_card_style())
        card_layout = QVBoxLayout(self.main_card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(20)
        
        # Başlık
        baslik = QLabel("🩸 Kan Şekeri Ölçümü")
        baslik.setStyleSheet(Styles.get_title_style())
        card_layout.addWidget(baslik, alignment=Qt.AlignCenter)
        
        # Değer girişi bölümü
        deger_frame = QFrame()
        deger_frame.setStyleSheet(Styles.get_inner_card_style())
        deger_layout = QVBoxLayout(deger_frame)
        
        # Değer başlık ve giriş
        deger_baslik = QLabel("📊 Ölçüm Değeri")
        deger_baslik.setStyleSheet(Styles.get_subtitle_style())
        deger_layout.addWidget(deger_baslik)
        
        deger_alt_baslik = QLabel("Kan şekeri değerinizi mg/dL cinsinden giriniz")
        deger_alt_baslik.setStyleSheet(Styles.get_label_style("#7f8c8d", 13))
        deger_layout.addWidget(deger_alt_baslik)
        
        self.kan_sekeri = QSpinBox()
        self.kan_sekeri.setRange(30, 500)
        self.kan_sekeri.setValue(120)
        self.kan_sekeri.setStyleSheet(Styles.get_modern_spinbox_style())
        deger_layout.addWidget(self.kan_sekeri)
        
        # Zaman bilgileri bölümü
        zaman_frame = QFrame()
        zaman_frame.setStyleSheet(Styles.get_inner_card_style())
        zaman_layout = QVBoxLayout(zaman_frame)
        
        zaman_baslik = QLabel("⏰ Ölçüm Zamanı")
        zaman_baslik.setStyleSheet(Styles.get_subtitle_style())
        zaman_layout.addWidget(zaman_baslik)
        
        # Öğün zamanı
        ogun_label = QLabel("Öğün durumu:")
        ogun_label.setStyleSheet(Styles.get_label_style())
        
        self.olcum_zamani = QComboBox()
        self.olcum_zamani.addItems([
            "Sabah", 
            "Öğle", 
            "İkindi", 
            "Akşam", 
            "Gece"
        ])
        self.olcum_zamani.setStyleSheet(Styles.get_modern_combobox_style())
        
        ogun_layout = QHBoxLayout()
        ogun_layout.addWidget(ogun_label)
        ogun_layout.addWidget(self.olcum_zamani)
        zaman_layout.addLayout(ogun_layout)
        
        # Tarih ve saat
        tarih_saat_layout = QHBoxLayout()
        
        tarih_layout = QVBoxLayout()
        tarih_label = QLabel("Tarih:")
        tarih_label.setStyleSheet(Styles.get_label_style())
        self.tarih = QDateEdit()
        self.tarih.setDate(QDate.currentDate())
        self.tarih.setCalendarPopup(True)
        self.tarih.setStyleSheet(Styles.get_modern_dateedit_style())
        tarih_layout.addWidget(tarih_label)
        tarih_layout.addWidget(self.tarih)
        
        saat_layout = QVBoxLayout()
        saat_label = QLabel("Saat:")
        saat_label.setStyleSheet(Styles.get_label_style())
        self.saat = QTimeEdit()
        self.saat.setTime(QTime.currentTime())
        self.saat.setStyleSheet(Styles.get_modern_timeedit_style())
        saat_layout.addWidget(saat_label)
        saat_layout.addWidget(self.saat)
        
        tarih_saat_layout.addLayout(tarih_layout)
        tarih_saat_layout.addLayout(saat_layout)
        zaman_layout.addLayout(tarih_saat_layout)
        
        # Kaydet buton bölümü
        buton_frame = QFrame()
        buton_frame.setStyleSheet(Styles.get_inner_card_style())
        buton_layout = QVBoxLayout(buton_frame)
        
        bilgi_label = QLabel("Ölçüm değerlerini kaydederek sağlık takibinizi yapabilirsiniz.")
        bilgi_label.setStyleSheet("font-size: 13px; color: #7f8c8d; font-style: italic; margin-bottom: 10px;")
        buton_layout.addWidget(bilgi_label)
        
        self.kaydet_btn = QPushButton("💾 Ölçümü Kaydet")
        self.kaydet_btn.setStyleSheet(Styles.get_success_button_style())
        self.kaydet_btn.clicked.connect(self.olcum_kaydet)
        buton_layout.addWidget(self.kaydet_btn)
        
        # Ana düzene ekleme
        card_layout.addWidget(deger_frame)
        card_layout.addWidget(zaman_frame)
        card_layout.addWidget(buton_frame)
        
        content_layout.addWidget(self.main_card)
        
        scroll_area.setWidget(content_widget)
        
        main_layout.addWidget(scroll_area)
    
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
            if self.dashboard:
                self.dashboard.verileri_guncelle()
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Ölçüm kaydedilirken bir hata oluştu: {str(e)}")

class DashboardPenceresi(QWidget):
    def __init__(self, hasta, db):
        super().__init__()
        self.hasta = hasta
        self.db = db
        
        layout = QVBoxLayout()
        
        baslik = QLabel("📊 Günlük Özet")
        baslik.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(baslik)
        
        # Grafik butonu ekle
        grafik_frame = QFrame()
        grafik_frame.setStyleSheet(Styles.get_inner_card_style())
        grafik_layout = QVBoxLayout(grafik_frame)
        
        self.grafik_btn = QPushButton("📈 Kan Şekeri Grafiğini Göster")
        self.grafik_btn.setStyleSheet(Styles.get_modern_button_style())
        self.grafik_btn.clicked.connect(self.grafik_goster)
        grafik_layout.addWidget(self.grafik_btn)
        
        layout.addWidget(grafik_frame)
        
        kan_sekeri_frame = QFrame()
        kan_sekeri_frame.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        kan_sekeri_layout = QVBoxLayout()
        
        self.kan_sekeri_label = QLabel("Günlük Kan Şekeri Ortalaması: -- mg/dL")
        self.kan_sekeri_label.setStyleSheet("color: white; font-size: 16px;")
        kan_sekeri_layout.addWidget(self.kan_sekeri_label)
        
        self.degerler_label = QLabel()
        self.degerler_label.setStyleSheet("color: white; font-size: 14px;")
        kan_sekeri_layout.addWidget(self.degerler_label)
        
        kan_sekeri_frame.setLayout(kan_sekeri_layout)
        layout.addWidget(kan_sekeri_frame)
        
        takip_frame = QFrame()
        takip_frame.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        takip_layout = QVBoxLayout()
        
        egzersiz_label = QLabel("Egzersiz Hedefi")
        egzersiz_label.setStyleSheet("color: white; font-size: 16px;")
        self.egzersiz_progress = QProgressBar()
        self.egzersiz_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #34495e;
                border-radius: 5px;
                text-align: center;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #3498db;
            }
        """)
        takip_layout.addWidget(egzersiz_label)
        takip_layout.addWidget(self.egzersiz_progress)
        
        diyet_label = QLabel("Diyet Hedefi")
        diyet_label.setStyleSheet("color: white; font-size: 16px;")
        self.diyet_progress = QProgressBar()
        self.diyet_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #34495e;
                border-radius: 5px;
                text-align: center;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #2ecc71;
            }
        """)
        takip_layout.addWidget(diyet_label)
        takip_layout.addWidget(self.diyet_progress)
        
        takip_frame.setLayout(takip_layout)
        layout.addWidget(takip_frame)
        
        insulin_frame = QFrame()
        insulin_frame.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        insulin_layout = QVBoxLayout()
        
        insulin_baslik = QLabel("💉 İnsülin Takibi")
        insulin_baslik.setStyleSheet("color: white; font-size: 16px;")
        insulin_layout.addWidget(insulin_baslik)
        
        # Tarih filtresi
        tarih_layout = QHBoxLayout()
        self.baslangic_tarihi = QDateEdit()
        self.baslangic_tarihi.setDate(QDate.currentDate().addDays(-7))
        self.baslangic_tarihi.setStyleSheet(Styles.get_modern_dateedit_style())
        
        self.bitis_tarihi = QDateEdit()
        self.bitis_tarihi.setDate(QDate.currentDate())
        self.bitis_tarihi.setStyleSheet(Styles.get_modern_dateedit_style())
        
        self.filtrele_btn = QPushButton("Filtrele")
        self.filtrele_btn.setStyleSheet(Styles.get_button_style())
        self.filtrele_btn.clicked.connect(self.insulin_filtrele)
        
        tarih_layout.addWidget(QLabel("Başlangıç:"))
        tarih_layout.addWidget(self.baslangic_tarihi)
        tarih_layout.addWidget(QLabel("Bitiş:"))
        tarih_layout.addWidget(self.bitis_tarihi)
        tarih_layout.addWidget(self.filtrele_btn)
        
        insulin_layout.addLayout(tarih_layout)
        
        self.insulin_listesi = QListWidget()
        self.insulin_listesi.setStyleSheet("""
            QListWidget {
                background-color: #34495e;
                border: none;
                border-radius: 5px;
                color: white;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #2c3e50;
            }
        """)
        insulin_layout.addWidget(self.insulin_listesi)
        
        insulin_frame.setLayout(insulin_layout)
        layout.addWidget(insulin_frame)
        
        self.setLayout(layout)
        self.verileri_guncelle()
    
    def grafik_goster(self):
        self.grafik_penceresi = GrafikPenceresi(self.hasta, self.db)
        self.grafik_penceresi.show()
    
    def verileri_guncelle(self):
        bugun = datetime.now().date()
        olcumler = self.db.get_patient_measurements(self.hasta['id'])
        bugun_olcumler = [o for o in olcumler if o[3].date() == bugun]
        
        if bugun_olcumler:
            ortalama = sum(o[4] for o in bugun_olcumler) / len(bugun_olcumler)
            
            # Günlük insülin önerisini kontrol et
            try:
                print(f"İnsülin önerisi kontrol ediliyor: Hasta ID={self.hasta['id']}, Tarih={bugun}")
                insulin_oneri = self.db.get_todays_insulin(self.hasta['id'], bugun)
                print(f"İnsülin önerisi sonucu: {insulin_oneri}")
                
                if insulin_oneri:
                    doz = insulin_oneri[4]  # doz_miktari
                    print(f"İnsülin doz miktarı: {doz}")
                    if doz > 0:
                        self.kan_sekeri_label.setText(f"<span style='color:#2c3e50;'>Günlük Kan Şekeri Ortalaması:</span> <b style='color:#e74c3c;'>{ortalama:.1f} mg/dL</b> &nbsp;&nbsp; <span style='color:#2c3e50;'>İnsülin Önerisi:</span> <b style='color:#3498db;'>{doz} ml</b>")
                        self.kan_sekeri_label.setTextFormat(Qt.RichText)
                    else:
                        self.kan_sekeri_label.setText(f"<span style='color:#2c3e50;'>Günlük Kan Şekeri Ortalaması:</span> <b style='color:#2ecc71;'>{ortalama:.1f} mg/dL</b> &nbsp;&nbsp; <span style='color:#2c3e50;'>İnsülin Önerisi:</span> <b style='color:#2ecc71;'>Önerilmez</b>")
                        self.kan_sekeri_label.setTextFormat(Qt.RichText)
                else:
                    print("İnsülin önerisi bulunamadı")
                    self.kan_sekeri_label.setText(f"<span style='color:#2c3e50;'>Günlük Kan Şekeri Ortalaması:</span> <b style='color:#e74c3c;'>{ortalama:.1f} mg/dL</b>")
                    self.kan_sekeri_label.setTextFormat(Qt.RichText)
            except Exception as e:
                print(f"İnsülin önerisi alınırken hata: {str(e)}")
                self.kan_sekeri_label.setText(f"<span style='color:#2c3e50;'>Günlük Kan Şekeri Ortalaması:</span> <b style='color:#e74c3c;'>{ortalama:.1f} mg/dL</b>")
                self.kan_sekeri_label.setTextFormat(Qt.RichText)
            
            degerler_text = "Günlük Ölçümler:\n"
            for olcum in bugun_olcumler:
                saat = olcum[3].time().strftime('%H:%M')
                deger = olcum[4]
                zamani = olcum[5]
                degerler_text += f"• {saat} ({zamani}): {deger} mg/dL\n"
            self.degerler_label.setText(degerler_text)
        else:
            self.kan_sekeri_label.setText("<span style='color:#7f8c8d;'>Günlük Kan Şekeri Ortalaması: -- mg/dL</span>")
            self.kan_sekeri_label.setTextFormat(Qt.RichText)
            self.degerler_label.setText("Bugün için ölçüm bulunmamaktadır.")
        
        egzersizler = self.db.get_patient_exercises(self.hasta['id'])
        bugun_egzersizler = [e for e in egzersizler if e[2] == bugun]
        egzersiz_hedefi = 3 # güncellenebilir.
        egzersiz_tamamlanan = sum(1 for e in bugun_egzersizler if e[4])
        self.egzersiz_progress.setValue(int((egzersiz_tamamlanan / egzersiz_hedefi) * 100))
        
        diyetler = self.db.get_patient_diets(self.hasta['id'])
        bugun_diyetler = [d for d in diyetler if d[2] == bugun]
        diyet_hedefi = 3  # güncellenebilir.
        diyet_tamamlanan = sum(1 for d in bugun_diyetler if d[4])
        self.diyet_progress.setValue(int((diyet_tamamlanan / diyet_hedefi) * 100))
        
        self.insulin_filtrele()
    
    def insulin_filtrele(self):
        baslangic = self.baslangic_tarihi.date().toPyDate()
        bitis = self.bitis_tarihi.date().toPyDate()
        
        insulinler = self.db.get_patient_insulin(self.hasta['id'], baslangic, bitis)
        
        self.insulin_listesi.clear()
        for insulin in insulinler:
            tarih = insulin[2].strftime('%d.%m.%Y')
            ortalama = insulin[3]
            doz = insulin[4]
            self.insulin_listesi.addItem(f"{tarih} - Ortalama: {ortalama:.1f} mg/dL, Doz: {doz} ml")

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
        self.dashboardButton = QPushButton("Gösterge Paneli", self)
        self.dashboardButton.setStyleSheet(Styles.get_button_style())

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
        
        button_layout.addWidget(self.dashboardButton)
        button_layout.addWidget(self.bilgilerimButton)
        button_layout.addWidget(self.olcumEkleButton)
        button_layout.addWidget(self.egzersizButton)
        button_layout.addWidget(self.diyetButton)
        button_layout.addWidget(self.belirtiButton)

        self.main_layout.addWidget(self.label)
        self.main_layout.addLayout(button_layout)
        
        self.stacked_widget = QStackedWidget()
        
        self.dashboard_widget = DashboardPenceresi(self.hasta, self.db)
        self.bilgilerim_widget = BilgilerimPenceresi(self.hasta, self.db)
        self.olcum_widget = KanSekeriOlcumPenceresi(self.hasta, self.db, self.dashboard_widget)
        self.egzersiz_widget = EgzersizTakipPenceresi(self.hasta, self.db, self.dashboard_widget)
        self.diyet_widget = DiyetTakipPenceresi(self.hasta, self.db, self.dashboard_widget)
        self.belirti_widget = BelirtiTakipPenceresi(self.hasta, self.db)
        
        self.stacked_widget.addWidget(self.dashboard_widget)
        self.stacked_widget.addWidget(self.bilgilerim_widget)
        self.stacked_widget.addWidget(self.olcum_widget)
        self.stacked_widget.addWidget(self.egzersiz_widget)
        self.stacked_widget.addWidget(self.diyet_widget)
        self.stacked_widget.addWidget(self.belirti_widget)
        
        self.main_layout.addWidget(self.stacked_widget)
        
        self.dashboardButton.clicked.connect(self.dashboard_goster)
        self.bilgilerimButton.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.olcumEkleButton.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.egzersizButton.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.diyetButton.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        self.belirtiButton.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))
        
        self.setLayout(self.main_layout)
    
    def dashboard_goster(self):
        self.dashboard_widget.verileri_guncelle()
        self.stacked_widget.setCurrentIndex(0)

