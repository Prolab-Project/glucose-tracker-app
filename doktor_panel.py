from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QListWidget, QPushButton, QLineEdit, QMessageBox, QComboBox, QFileDialog, QGraphicsPixmapItem, QHBoxLayout, QStackedWidget, QDialog, QFrame, QSpinBox, QDateEdit, QTimeEdit
from PyQt5.QtGui import QRegularExpressionValidator, QPixmap
from PyQt5.QtCore import QRegularExpression, Qt, QDate, QTime
from datetime import datetime, timedelta
import hashlib
from styles import Styles
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

EMAIL_GONDEREN = "bedirhanudemy@gmail.com"  
EMAIL_SIFRE = "gsle jctp mhzo fccz" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

class HastaListePenceresi(QWidget):    
    def __init__(self, doktor, db):
        super().__init__()

        self.setWindowTitle("Hastalarım")    
        self.setGeometry(100,100,400,200)
        self.doktor = doktor
        self.db = db
        self.hasta_listesi = QListWidget()
        self.hasta_listesi.setFixedWidth(600)
        self.hasta_listesi.setStyleSheet("font-size: 16px; padding: 8px;")
        self.layout = QHBoxLayout()  

        sol_layout = QVBoxLayout()

        # Filtreleme bölümü
        filtre_frame = QFrame()
        filtre_frame.setStyleSheet(Styles.get_inner_card_style())
        filtre_layout = QVBoxLayout(filtre_frame)
        
        filtre_baslik = QLabel("🔍 Hastaları Filtrele")
        filtre_baslik.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        filtre_layout.addWidget(filtre_baslik)
        
        # Kan şekeri filtreleme
        kan_sekeri_layout = QHBoxLayout()
        kan_sekeri_layout.addWidget(QLabel("Kan Şekeri:"))
        
        self.kan_sekeri_filtre = QComboBox()
        self.kan_sekeri_filtre.addItems([
            "Hepsi", 
            "Düşük (<70 mg/dL)", 
            "Normal (70-110 mg/dL)",
            "Yüksek Normal (111-150 mg/dL)",
            "Yüksek (151-200 mg/dL)",
            "Çok Yüksek (>200 mg/dL)"
        ])
        self.kan_sekeri_filtre.setStyleSheet(Styles.get_modern_combobox_style())
        kan_sekeri_layout.addWidget(self.kan_sekeri_filtre)
        
        # Belirti filtreleme
        belirti_layout = QHBoxLayout()
        belirti_layout.addWidget(QLabel("Belirti:"))
        
        self.belirti_filtre = QComboBox()
        self.belirti_filtre.addItems([
            "Hepsi",
            "Poliüri (Sık idrara çıkma)",
            "Polifaji (Aşırı açlık hissi)",
            "Polidipsi (Aşırı susama hissi)",
            "Nöropati (El ve ayaklarda karıncalanma veya uyuşma hissi)",
            "Kilo kaybı",
            "Yorgunluk",
            "Yaraların yavaş iyileşmesi",
            "Bulanık görme"
        ])
        self.belirti_filtre.setStyleSheet(Styles.get_modern_combobox_style())
        belirti_layout.addWidget(self.belirti_filtre)
        
        # Tarih filtreleme
        tarih_layout = QHBoxLayout()
        tarih_layout.addWidget(QLabel("Tarih:"))
        
        self.tarih_filtre = QComboBox()
        self.tarih_filtre.addItems([
            "Hepsi",
            "Bugün",
            "Son 3 Gün",
            "Son 7 Gün",
            "Son 30 Gün"
        ])
        self.tarih_filtre.setStyleSheet(Styles.get_modern_combobox_style())
        tarih_layout.addWidget(self.tarih_filtre)
        
        # Filtreleme butonları
        buton_layout = QHBoxLayout()
        
        self.uygula_btn = QPushButton("Filtreleri Uygula")
        self.uygula_btn.setStyleSheet(Styles.get_button_style())
        self.uygula_btn.clicked.connect(self.hastalari_getir)
        
        self.temizle_btn = QPushButton("Filtreleri Temizle")
        self.temizle_btn.setStyleSheet(Styles.get_button_style())
        self.temizle_btn.clicked.connect(self.filtreleri_temizle)
        
        buton_layout.addWidget(self.uygula_btn)
        buton_layout.addWidget(self.temizle_btn)
        
        filtre_layout.addLayout(kan_sekeri_layout)
        filtre_layout.addLayout(belirti_layout)
        filtre_layout.addLayout(tarih_layout)
        filtre_layout.addLayout(buton_layout)
        
        self.detay_paneli = QWidget()
        self.detay_paneli.setFixedWidth(300)  # Hasta bilgileri panelinin genişliğini sınırla
        self.detay_layout = QVBoxLayout()
        
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
        
        self.detay_label = QLabel("Hasta bilgileri burada görünecek")
        self.detay_layout.addWidget(self.profil_foto, alignment=Qt.AlignCenter)
        self.detay_layout.addWidget(self.detay_label)
        
        self.olcum_ekle_btn = QPushButton("➕ Ölçüm Ekle")
        self.olcum_ekle_btn.setStyleSheet(Styles.get_button_style())
        self.olcum_ekle_btn.clicked.connect(self.olcum_ekle)
        
        self.goruntule_btn = QPushButton("📊 Ölçümleri Görüntüle")
        self.goruntule_btn.setStyleSheet(Styles.get_button_style())
        self.goruntule_btn.clicked.connect(self.olcumleri_goruntule)

        self.diyet_goruntule_btn = QPushButton("🍽️ Diyet Takibi")
        self.diyet_goruntule_btn.setStyleSheet(Styles.get_button_style())
        self.diyet_goruntule_btn.clicked.connect(self.diyet_goruntule)
        
        self.insulin_oneri_btn = QPushButton("💉 İnsülin Öneri")
        self.insulin_oneri_btn.setStyleSheet(Styles.get_button_style())
        self.insulin_oneri_btn.clicked.connect(self.insulin_oneri)
        
        self.belirti_ekle_btn = QPushButton("⚠️ Belirti Ekle")
        self.belirti_ekle_btn.setStyleSheet(Styles.get_button_style())
        self.belirti_ekle_btn.clicked.connect(self.belirti_ekle)
        
        self.belirti_goruntule_btn = QPushButton("📋 Belirtileri Görüntüle")
        self.belirti_goruntule_btn.setStyleSheet(Styles.get_button_style())
        self.belirti_goruntule_btn.clicked.connect(self.belirtileri_goruntule)
        
        self.diyet_egzersiz_btn = QPushButton("🔄 Diyet & Egzersiz Öneri")
        self.diyet_egzersiz_btn.setStyleSheet(Styles.get_button_style())
        self.diyet_egzersiz_btn.clicked.connect(self.diyet_egzersiz_oneri_goster)
                
        # Yeni grafik gösterim butonu
        self.grafik_goster_btn = QPushButton("📈 Grafiksel Analiz")
        self.grafik_goster_btn.setStyleSheet(Styles.get_button_style())
        self.grafik_goster_btn.clicked.connect(self.grafik_goster)
        
        self.olcum_ekle_btn.setEnabled(False)
        self.goruntule_btn.setEnabled(False)
        self.guncelle_btn.setEnabled(False)
        self.diyet_goruntule_btn.setEnabled(False)
        self.insulin_oneri_btn.setEnabled(False)
        self.belirti_ekle_btn.setEnabled(False)
        self.belirti_goruntule_btn.setEnabled(False)
        self.diyet_egzersiz_btn.setEnabled(False)
        self.grafik_goster_btn.setEnabled(False)
        
        self.detay_layout.addWidget(self.olcum_ekle_btn)
        self.detay_layout.addWidget(self.goruntule_btn)
        self.detay_layout.addWidget(self.diyet_goruntule_btn)
        self.detay_layout.addWidget(self.insulin_oneri_btn)
        self.detay_layout.addWidget(self.belirti_ekle_btn)
        self.detay_layout.addWidget(self.belirti_goruntule_btn)
        self.detay_layout.addWidget(self.diyet_egzersiz_btn)
        self.detay_layout.addWidget(self.grafik_goster_btn)  # Yeni buton eklendi
        self.detay_layout.addWidget(self.guncelle_btn)

        baslik_label = QLabel("🩺 Hastalarım")
        baslik_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")
        self.detay_label.setStyleSheet("color: black; font-size: 16px;")

        sol_layout.addWidget(baslik_label)
        sol_layout.addWidget(filtre_frame)  # Filtreleme panelini ekle
        sol_layout.addWidget(self.hasta_listesi)
        self.detay_paneli.setLayout(self.detay_layout)
        self.layout.addWidget(self.detay_paneli)
        self.layout.addLayout(sol_layout)
        self.setLayout(self.layout)
        self.hastalari_getir()

        self.hasta_listesi.itemClicked.connect(self.hasta_detaylarini_goster)
        
        self.secili_hasta_id = None
        self.secili_hasta = None

    def hastalari_getir(self):
        self.hasta_listesi.clear()  
        
        # Filtreleri al
        kan_sekeri_filtre = self.kan_sekeri_filtre.currentText()
        belirti_filtre = self.belirti_filtre.currentText()
        tarih_filtre = self.tarih_filtre.currentText()
        
        # Tüm hastaları al
        hastalar = self.db.get_doctor_patients(self.doktor['id'])
        filtrelenmis_hastalar = []
        
        for hasta in hastalar:
            hasta_id = hasta[0]
            eklenecek = True
            
            # Kan şekeri filtresini uygula
            if kan_sekeri_filtre != "Hepsi":
                olcumler = self.db.get_patient_measurements(hasta_id)
                if olcumler:
                    # Son ölçüm yerine tüm ölçümlerin ortalamasını hesapla
                    toplam_kan_sekeri = 0
                    olcum_sayisi = 0
                    
                    for olcum in olcumler:
                        toplam_kan_sekeri += olcum[4]  # olcum[4] = kan_seker_degeri
                        olcum_sayisi += 1
                    
                    # Ortalama kan şekeri değeri
                    ortalama_kan_sekeri = toplam_kan_sekeri / olcum_sayisi if olcum_sayisi > 0 else 0
                    
                    # Ortalama değere göre filtreleme yap
                    if kan_sekeri_filtre == "Düşük (<70 mg/dL)" and ortalama_kan_sekeri >= 70:
                        eklenecek = False
                    elif kan_sekeri_filtre == "Normal (70-110 mg/dL)" and (ortalama_kan_sekeri < 70 or ortalama_kan_sekeri > 110):
                        eklenecek = False
                    elif kan_sekeri_filtre == "Yüksek Normal (111-150 mg/dL)" and (ortalama_kan_sekeri < 111 or ortalama_kan_sekeri > 150):
                        eklenecek = False
                    elif kan_sekeri_filtre == "Yüksek (151-200 mg/dL)" and (ortalama_kan_sekeri < 151 or ortalama_kan_sekeri > 200):
                        eklenecek = False
                    elif kan_sekeri_filtre == "Çok Yüksek (>200 mg/dL)" and ortalama_kan_sekeri <= 200:
                        eklenecek = False
                else:
                    # Ölçüm yoksa ve filtre uygulanıyorsa, hastayı listeye alma
                    if kan_sekeri_filtre != "Hepsi":
                        eklenecek = False
            
            # Belirti filtresini uygula
            if eklenecek and belirti_filtre != "Hepsi":
                belirtiler = self.db.get_patient_symptoms(hasta_id)
                belirti_var = False
                
                for belirti in belirtiler:
                    if belirti[3] == belirti_filtre:
                        belirti_var = True
                        break
                
                if not belirti_var:
                    eklenecek = False
            
            # Tarih filtresini uygula
            if eklenecek and tarih_filtre != "Hepsi":
                olcumler = self.db.get_patient_measurements(hasta_id)
                tarih_filtresine_uyuyor = False
                
                if olcumler:
                    bugun = datetime.now().date()
                    
                    for olcum in olcumler:
                        olcum_tarihi = olcum[3].date()
                        fark = (bugun - olcum_tarihi).days
                        
                        if tarih_filtre == "Bugün" and fark == 0:
                            tarih_filtresine_uyuyor = True
                            break
                        elif tarih_filtre == "Son 3 Gün" and fark <= 2:
                            tarih_filtresine_uyuyor = True
                            break
                        elif tarih_filtre == "Son 7 Gün" and fark <= 6:
                            tarih_filtresine_uyuyor = True
                            break
                        elif tarih_filtre == "Son 30 Gün" and fark <= 29:
                            tarih_filtresine_uyuyor = True
                            break
                
                if not tarih_filtresine_uyuyor:
                    eklenecek = False
            
            if eklenecek:
                filtrelenmis_hastalar.append(hasta)
        
        # Filtrelenmiş hastaları listele
        for hasta in filtrelenmis_hastalar:
            self.hasta_listesi.addItem(f"{hasta[2]} {hasta[3]} - TC: {hasta[1]}")
        
        # Filtre sonuçlarını göster
        if not filtrelenmis_hastalar:
            self.hasta_listesi.addItem("Filtrelere uygun hasta bulunamadı.")
    
    def filtreleri_temizle(self):
        self.kan_sekeri_filtre.setCurrentIndex(0)  # "Hepsi" seçeneği
        self.belirti_filtre.setCurrentIndex(0)     # "Hepsi" seçeneği
        self.tarih_filtre.setCurrentIndex(0)       # "Hepsi" seçeneği
        self.hastalari_getir()  # Filtreleri temizleyip listeyi yenile
    
    def olcum_ekle(self):
        if not self.secili_hasta_id or not self.secili_hasta:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir hasta seçin.")
            return
            
        dialog = QDialog(self)
        dialog.setWindowTitle(f"{self.secili_hasta['ad']} {self.secili_hasta['soyad']} - Kan Şekeri Ölçümü Ekle")
        dialog.setMinimumSize(400, 500) 
        
        main_layout = QVBoxLayout(dialog)
        main_layout.setContentsMargins(10, 10, 10, 10)  # Kenar boşluklarını azalt
        main_layout.setSpacing(10)
        
        # Ana kart frame
        main_card = QFrame()
        main_card.setStyleSheet(Styles.get_modern_card_style())
        card_layout = QVBoxLayout(main_card)
        card_layout.setContentsMargins(15, 15, 15, 15)  
        card_layout.setSpacing(10) 
        
        baslik = QLabel("🩸 Kan Şekeri Ölçümü")
        baslik.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        card_layout.addWidget(baslik, alignment=Qt.AlignCenter)
        
        hasta_bilgisi = QLabel(f"Hasta: {self.secili_hasta['ad']} {self.secili_hasta['soyad']}")
        hasta_bilgisi.setStyleSheet("font-size: 14px; color: #3498db;")
        card_layout.addWidget(hasta_bilgisi, alignment=Qt.AlignCenter)
        
        deger_frame = QFrame()
        deger_frame.setStyleSheet(Styles.get_inner_card_style())
        deger_layout = QVBoxLayout(deger_frame)
        deger_layout.setContentsMargins(10, 10, 10, 10)  # Kenar boşluklarını azalt
        deger_layout.setSpacing(5)  # Azalt
        
        deger_baslik = QLabel("📊 Ölçüm Değeri")
        deger_baslik.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        deger_layout.addWidget(deger_baslik)
        
        kan_sekeri = QSpinBox()
        kan_sekeri.setRange(30, 500)
        kan_sekeri.setValue(120)
        kan_sekeri.setStyleSheet("""
            QSpinBox {
                border: 1px solid #3498db;
                border-radius: 5px;
                padding: 5px;
                background-color: white;
                font-size: 14px;
                min-height: 25px;
            }
        """)
        deger_layout.addWidget(kan_sekeri)
        
        zaman_frame = QFrame()
        zaman_frame.setStyleSheet(Styles.get_inner_card_style())
        zaman_layout = QVBoxLayout(zaman_frame)
        zaman_layout.setContentsMargins(10, 10, 10, 10)  
        zaman_layout.setSpacing(5)  
        zaman_baslik = QLabel("⏰ Ölçüm Zamanı")
        zaman_baslik.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        zaman_layout.addWidget(zaman_baslik)
        
        ogun_layout = QHBoxLayout()
        ogun_label = QLabel("Öğün:")
        ogun_label.setStyleSheet("font-size: 12px;")
        olcum_zamani = QComboBox()
        olcum_zamani.addItems([
            "Sabah", 
            "Öğle", 
            "İkindi", 
            "Akşam", 
            "Gece"
        ])
        olcum_zamani.setStyleSheet("""
            QComboBox {
                border: 1px solid #3498db;
                border-radius: 5px;
                padding: 3px;
                background-color: white;
                font-size: 12px;
                min-height: 25px;
            }
        """)
        
        ogun_layout.addWidget(ogun_label)
        ogun_layout.addWidget(olcum_zamani)
        zaman_layout.addLayout(ogun_layout)
        
        tarih_saat_layout = QHBoxLayout()
        
        tarih_layout = QVBoxLayout()
        tarih_label = QLabel("Tarih:")
        tarih_label.setStyleSheet("font-size: 12px;")
        tarih = QDateEdit()
        tarih.setDate(QDate.currentDate())
        tarih.setCalendarPopup(True)
        tarih.setStyleSheet("""
            QDateEdit {
                border: 1px solid #3498db;
                border-radius: 5px;
                padding: 3px;
                background-color: white;
                font-size: 12px;
                min-height: 25px;
            }
        """)
        tarih_layout.addWidget(tarih_label)
        tarih_layout.addWidget(tarih)
        
        saat_layout = QVBoxLayout()
        saat_label = QLabel("Saat:")
        saat_label.setStyleSheet("font-size: 12px;")
        saat = QTimeEdit()
        saat.setTime(QTime.currentTime())
        saat.setStyleSheet("""
            QTimeEdit {
                border: 1px solid #3498db;
                border-radius: 5px;
                padding: 3px;
                background-color: white;
                font-size: 12px;
                min-height: 25px;
            }
        """)
        saat_layout.addWidget(saat_label)
        saat_layout.addWidget(saat)
        
        tarih_saat_layout.addLayout(tarih_layout)
        tarih_saat_layout.addLayout(saat_layout)
        zaman_layout.addLayout(tarih_saat_layout)
        
        buton_layout = QHBoxLayout()  
        
        kaydet_btn = QPushButton("Kaydet")
        kaydet_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 13px;
            }
        """)
        
        # Kaydetme işlemini lambda fonksiyon olarak tanımlayalım
        kaydet_btn.clicked.connect(lambda: self.olcum_kaydet_dialog(
            dialog, 
            self.secili_hasta_id, 
            kan_sekeri.value(),
            olcum_zamani.currentText(),
            tarih.date().toPyDate(),
            saat.time().toPyTime()
        ))
        
        iptal_btn = QPushButton("İptal")
        iptal_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 13px;
            }
        """)
        iptal_btn.clicked.connect(dialog.reject)
        
        buton_layout.addWidget(kaydet_btn)
        buton_layout.addWidget(iptal_btn)
        
        card_layout.addWidget(deger_frame)
        card_layout.addWidget(zaman_frame)
        card_layout.addLayout(buton_layout)  
        
        main_layout.addWidget(main_card)
        
        dialog.exec_()
    
    def olcum_kaydet_dialog(self, dialog, hasta_id, kan_sekeri_degeri, olcum_zamani, tarih, saat):
        try:
            from datetime import datetime
            tarih_saat = datetime.combine(tarih, saat)
            
            self.db.add_measurement(
                hasta_id,
                self.doktor['id'],  # doktor_id burada doktor olarak ekleniyor
                kan_sekeri_degeri,
                olcum_zamani
            )
            QMessageBox.information(self, "Başarılı", "Kan şekeri ölçümü kaydedildi.")
            dialog.accept()
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Ölçüm kaydedilirken bir hata oluştu: {str(e)}")
        
    def olcumleri_goruntule(self):
        if not self.secili_hasta_id:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir hasta seçin.")
            return
        
        olcumler = self.db.get_patient_measurements(self.secili_hasta_id)
        
        if not olcumler:
            QMessageBox.information(self, "Bilgi", "Bu hasta için kaydedilmiş ölçüm bulunmamaktadır.")
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Hasta Ölçümleri")
        dialog.setMinimumSize(600, 400)
        
        layout = QVBoxLayout()
        
        hasta = self.db.get_user_by_id(self.secili_hasta_id)
        if hasta:
            baslik = QLabel(f"{hasta[2]} {hasta[3]} - Kan Şekeri Ölçümleri")
        else:
            baslik = QLabel("Kan Şekeri Ölçümleri")
        baslik.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(baslik)
        
        liste = QListWidget()
        liste.setStyleSheet("""
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 14px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
        """)
        
        for olcum in olcumler:
            tarih_saat = olcum[3].strftime("%d.%m.%Y %H:%M")
            deger = olcum[4]
            zaman = olcum[5] if olcum[5] else "Belirtilmemiş"
            
            item_text = f"{tarih_saat} - {deger} mg/dL ({zaman})"
            liste.addItem(item_text)
        
        layout.addWidget(liste)
        
        if olcumler:
            toplam_deger = sum(o[4] for o in olcumler)
            ortalama = toplam_deger / len(olcumler)
            
            ortalama_label = QLabel(f"Ortalama Kan Şekeri: {ortalama:.1f} mg/dL (Toplam {len(olcumler)} ölçüm)")
            ortalama_label.setStyleSheet("font-size: 16px; margin-top: 10px;")
            layout.addWidget(ortalama_label)
        
        kapat_btn = QPushButton("Kapat")
        kapat_btn.setStyleSheet(Styles.get_button_style())
        kapat_btn.clicked.connect(dialog.close)
        
        layout.addWidget(kapat_btn, alignment=Qt.AlignCenter)
        
        dialog.setLayout(layout)
        dialog.exec_()

    def diyet_goruntule(self): 
        if not self.secili_hasta_id : 
            QMessageBox.warning(self, "Uyarı", "Lutfen bir hasta seçiniz.")
            return
        try:
            diyetler = self.db.get_patient_diets(self.secili_hasta_id)
            if not diyetler : 
                cevap = QMessageBox.question(self, "Bilgi", 
                    f"Bu hasta (ID: {self.secili_hasta_id}) için diyet bilgisi bulunamamıştır.\nYeni diyet eklemek ister misiniz?",
                    QMessageBox.Yes | QMessageBox.No
                )
                
                if cevap == QMessageBox.Yes:
                    self.diyet_ekle()
                return
            
            dialog = QDialog(self) 
            dialog.setWindowTitle("Hasta diyet bilgileri")
            dialog.setMinimumSize(600,400)

            layout = QVBoxLayout() 

            hasta = self.db.get_user_by_id(self.secili_hasta_id)
            if hasta:
                baslik = QLabel(f"{hasta[2]} {hasta[3]} - Diyet Bilgileri")
            else : 
                baslik= QLabel("Diyet bilgileri")        
            baslik.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
            layout.addWidget(baslik)
            
            liste = QListWidget()
            liste.setStyleSheet("""
                QListWidget {
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    font-size: 14px;
                    padding: 5px;
                }
                QListWidget::item {
                    padding: 8px;
                    border-bottom: 1px solid #eee;
                }
            """)        
            for diyet in diyetler:
                tarih = diyet[2].strftime("%d.%m.%Y")
                diyet_turu = diyet[3]
                diyet_uygulandi = diyet[4] 
                
                item_text= f"{tarih} - Diyet Türü: {diyet_turu} - Diyet Uygulandı Mı? {'Evet' if diyet_uygulandi else 'Hayır'}"
                liste.addItem(item_text)
            
            layout.addWidget(liste)
            
            # Butonlar
            buton_layout = QHBoxLayout()
            
            yeni_ekle_btn = QPushButton("Yeni Diyet Ekle")
            yeni_ekle_btn.setStyleSheet(Styles.get_button_style())
            yeni_ekle_btn.clicked.connect(lambda: [dialog.close(), self.diyet_ekle()])
            
            kapat_btn = QPushButton("Kapat")
            kapat_btn.setStyleSheet(Styles.get_button_style())
            kapat_btn.clicked.connect(dialog.close)
            
            buton_layout.addWidget(yeni_ekle_btn)
            buton_layout.addWidget(kapat_btn)
            
            layout.addLayout(buton_layout)
            
            dialog.setLayout(layout)
            dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Diyet bilgileri görüntülenirken bir hata oluştu:\n{str(e)}")

    def diyet_ekle(self):
        if not self.secili_hasta_id or not self.secili_hasta:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir hasta seçin.")
            return
            
        dialog = QDialog(self)
        dialog.setWindowTitle(f"{self.secili_hasta['ad']} {self.secili_hasta['soyad']} - Diyet Ekle")
        dialog.setMinimumSize(400, 500) 
        
        main_layout = QVBoxLayout(dialog)
        main_layout.setContentsMargins(10, 10, 10, 10)  # Kenar boşluklarını azalt
        main_layout.setSpacing(10)
        
        # Ana kart frame
        main_card = QFrame()
        main_card.setStyleSheet(Styles.get_modern_card_style())
        card_layout = QVBoxLayout(main_card)
        card_layout.setContentsMargins(15, 15, 15, 15)  
        card_layout.setSpacing(10) 
        
        baslik = QLabel("🍽 Diyet Ekle")
        baslik.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        card_layout.addWidget(baslik, alignment=Qt.AlignCenter)
        
        hasta_bilgisi = QLabel(f"Hasta: {self.secili_hasta['ad']} {self.secili_hasta['soyad']}")
        hasta_bilgisi.setStyleSheet("font-size: 14px; color: #3498db;")
        card_layout.addWidget(hasta_bilgisi, alignment=Qt.AlignCenter)
        
        # Tarih seçimi
        tarih_frame = QFrame()
        tarih_frame.setStyleSheet(Styles.get_inner_card_style())
        tarih_layout = QVBoxLayout(tarih_frame)
        
        tarih_baslik = QLabel("📅 Tarih")
        tarih_baslik.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        tarih_layout.addWidget(tarih_baslik)
        
        tarih = QDateEdit()
        tarih.setDate(QDate.currentDate())
        tarih.setCalendarPopup(True)
        tarih.setStyleSheet("""
            QDateEdit {
                border: 1px solid #3498db;
                border-radius: 5px;
                padding: 3px;
                background-color: white;
                font-size: 12px;
                min-height: 25px;
            }
        """)
        tarih_layout.addWidget(tarih)
        
        # Diyet türü seçimi
        diyet_frame = QFrame()
        diyet_frame.setStyleSheet(Styles.get_inner_card_style())
        diyet_layout = QVBoxLayout(diyet_frame)
        
        diyet_baslik = QLabel("🥗 Diyet Türü")
        diyet_baslik.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        diyet_layout.addWidget(diyet_baslik)
        
        diyet_turu = QComboBox()
        diyet_turu.addItems(["Az Şekerli Diyet", "Şekersiz Diyet", "Dengeli Beslenme"])
        diyet_turu.setStyleSheet("""
            QComboBox {
                border: 1px solid #3498db;
                border-radius: 5px;
                padding: 3px;
                background-color: white;
                font-size: 12px;
                min-height: 25px;
            }
        """)
        diyet_layout.addWidget(diyet_turu)
        
        # Diyet durumu
        durum_frame = QFrame()
        durum_frame.setStyleSheet(Styles.get_inner_card_style())
        durum_layout = QVBoxLayout(durum_frame)
        
        durum_baslik = QLabel("✅ Diyet Durumu")
        durum_baslik.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        durum_layout.addWidget(durum_baslik)
        
        diyet_uygulandi = QComboBox()
        diyet_uygulandi.addItems(["Uygulandı", "Uygulanmadı"])
        diyet_uygulandi.setStyleSheet("""
            QComboBox {
                border: 1px solid #3498db;
                border-radius: 5px;
                padding: 3px;
                background-color: white;
                font-size: 12px;
                min-height: 25px;
            }
        """)
        durum_layout.addWidget(diyet_uygulandi)
        
        buton_layout = QHBoxLayout()  
        
        kaydet_btn = QPushButton("Kaydet")
        kaydet_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 13px;
            }
        """)
        
        kaydet_btn.clicked.connect(lambda: self.diyet_kaydet_dialog(
            dialog, 
            self.secili_hasta_id, 
            tarih.date().toPyDate(),
            diyet_turu.currentText(),
            diyet_uygulandi.currentText() == "Uygulandı"
        ))
        
        iptal_btn = QPushButton("İptal")
        iptal_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 13px;
            }
        """)
        iptal_btn.clicked.connect(dialog.reject)
        
        buton_layout.addWidget(kaydet_btn)
        buton_layout.addWidget(iptal_btn)
        
        # Kartları ana karta ekle
        card_layout.addWidget(tarih_frame)
        card_layout.addWidget(diyet_frame)
        card_layout.addWidget(durum_frame)
        card_layout.addLayout(buton_layout)  
        
        main_layout.addWidget(main_card)
        
        dialog.exec_()
    
    def diyet_kaydet_dialog(self, dialog, hasta_id, tarih, diyet_turu, diyet_uygulandi):
        try:
            self.db.add_diet(
                hasta_id,
                tarih,
                diyet_turu,
                diyet_uygulandi
            )
            QMessageBox.information(self, "Başarılı", "Diyet kaydedildi.")
            dialog.accept()
            # Diyet listesini yenilemek için yeniden görüntüleme
            self.diyet_goruntule()
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Diyet kaydedilirken bir hata oluştu: {str(e)}")

    def hasta_detaylarini_goster(self, item):
        tc = item.text().split("TC: ")[-1]
        hasta = self.db.get_user_by_tc(tc, None)  

        if hasta:
            self.secili_hasta_id = hasta[0]
            self.secili_hasta = {
                'id': hasta[0],
                'tc_kimlik_no': hasta[1],
                'ad': hasta[2],
                'soyad': hasta[3],
                'dogum_tarihi': hasta[4],
                'sifre_hash': hasta[5],
                'cinsiyet': hasta[6],
                'rol': hasta[7],
                'eposta': hasta[8],
                'profil_resmi': hasta[9]
            }
            
            if self.secili_hasta['profil_resmi']:
                pixmap = QPixmap()
                pixmap.loadFromData(self.secili_hasta['profil_resmi'])
                rounded_pixmap = QPixmap(pixmap.size())
                rounded_pixmap.fill(Qt.transparent)
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
                f"<b>Ad:</b> {self.secili_hasta['ad']}<br>"
                f"<b>Soyad:</b> {self.secili_hasta['soyad']}<br>"
                f"<b>TC:</b> {self.secili_hasta['tc_kimlik_no']}<br>"
                f"<b>Email:</b> {self.secili_hasta['eposta']}<br>"
                f"<b>Doğum Tarihi:</b> {self.secili_hasta['dogum_tarihi'].strftime('%d.%m.%Y')}<br>"
            )
            self.detay_label.setText(detay)
            
            self.olcum_ekle_btn.setEnabled(True)
            self.goruntule_btn.setEnabled(True)
            self.guncelle_btn.setEnabled(True)
            self.diyet_goruntule_btn.setEnabled(True)
            self.insulin_oneri_btn.setEnabled(True)
            self.belirti_ekle_btn.setEnabled(True)
            self.belirti_goruntule_btn.setEnabled(True)
            self.diyet_egzersiz_btn.setEnabled(True)
            self.grafik_goster_btn.setEnabled(True)  # Yeni buton aktif edildi



    def insulin_oneri(self):
        if not self.secili_hasta_id or not self.secili_hasta:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir hasta seçin.")
            return
        
        try:
            olcumler = self.db.get_patient_measurements(self.secili_hasta_id)
            bugun = datetime.now().date()
            bugun_olcumler = [o for o in olcumler if o[3].date() == bugun]
            
            if not bugun_olcumler:
                cevap = QMessageBox.question(
                    self, 
                    "Uyarı", 
                    "Bugün için ölçüm bulunmamaktadır. Geçmiş tarihli bir ölçüm için öneri yapmak ister misiniz?",
                    QMessageBox.Yes | QMessageBox.No
                )
                
                if cevap == QMessageBox.Yes:
                    self.insulin_oneri_tarih_sec()
                return
            
            self.insulin_hesapla(bugun_olcumler)
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"İnsülin önerisi oluşturulurken bir hata oluştu:\n{str(e)}")
    
    def insulin_oneri_tarih_sec(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Tarih Seçin")
        dialog.setMinimumWidth(300)
        
        layout = QVBoxLayout()
        
        tarih_label = QLabel("İnsülin önerisi için tarih seçin:")
        tarih = QDateEdit()
        tarih.setDate(QDate.currentDate())
        tarih.setCalendarPopup(True)
        tarih.setMaximumDate(QDate.currentDate())
        tarih.setStyleSheet(Styles.get_modern_dateedit_style())
        
        buton_layout = QHBoxLayout()
        tamam_btn = QPushButton("Tamam")
        tamam_btn.setStyleSheet(Styles.get_button_style())
        tamam_btn.clicked.connect(lambda: self.secili_tarih_olcumleri_al(dialog, tarih.date()))
        
        iptal_btn = QPushButton("İptal")
        iptal_btn.setStyleSheet(Styles.get_button_style())
        iptal_btn.clicked.connect(dialog.reject)
        
        buton_layout.addWidget(tamam_btn)
        buton_layout.addWidget(iptal_btn)
        
        layout.addWidget(tarih_label)
        layout.addWidget(tarih)
        layout.addLayout(buton_layout)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def secili_tarih_olcumleri_al(self, dialog, tarih):
        secili_tarih = tarih.toPyDate()
        
        olcumler = self.db.get_patient_measurements(self.secili_hasta_id)
        secili_tarih_olcumler = [o for o in olcumler if o[3].date() == secili_tarih]
        
        if not secili_tarih_olcumler:
            QMessageBox.warning(self, "Uyarı", f"{secili_tarih.strftime('%d.%m.%Y')} tarihinde ölçüm bulunmamaktadır.")
            return
        
        dialog.accept()
        self.insulin_hesapla(secili_tarih_olcumler)
    
    def insulin_hesapla(self, olcumler):
        sabah_olcumler = []
        ogle_olcumler = []
        ikindi_olcumler = []
        aksam_olcumler = []
        gece_olcumler = []
        
        for olcum in olcumler:
            olcum_zamani = olcum[5] if olcum[5] else ""
            kan_seker_degeri = olcum[4]
            ortalamaya_dahil = olcum[6]
            
            if not ortalamaya_dahil:
                continue
                
            if "Sabah" in olcum_zamani:
                sabah_olcumler.append(kan_seker_degeri)
            elif "Öğle" in olcum_zamani:
                ogle_olcumler.append(kan_seker_degeri)
            elif "İkindi" in olcum_zamani:
                ikindi_olcumler.append(kan_seker_degeri)
            elif "Akşam" in olcum_zamani:
                aksam_olcumler.append(kan_seker_degeri)
            elif "Gece" in olcum_zamani:
                gece_olcumler.append(kan_seker_degeri)
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"İnsülin Önerisi - {self.secili_hasta['ad']} {self.secili_hasta['soyad']}")
        dialog.setMinimumSize(600, 500)
        
        main_layout = QVBoxLayout()
        
        main_card = QFrame()
        main_card.setStyleSheet(Styles.get_modern_card_style())
        card_layout = QVBoxLayout(main_card)
        
        baslik = QLabel("💉 İnsülin Doz Önerisi")
        baslik.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        card_layout.addWidget(baslik, alignment=Qt.AlignCenter)
        
        hasta_bilgisi = QLabel(f"Hasta: {self.secili_hasta['ad']} {self.secili_hasta['soyad']}")
        hasta_bilgisi.setStyleSheet("font-size: 16px; color: #3498db;")
        card_layout.addWidget(hasta_bilgisi, alignment=Qt.AlignCenter)
        
        tarih = olcumler[0][3].date() if olcumler else datetime.now().date()
        tarih_bilgisi = QLabel(f"Tarih: {tarih.strftime('%d.%m.%Y')}")
        tarih_bilgisi.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        card_layout.addWidget(tarih_bilgisi, alignment=Qt.AlignCenter)
        
        tablo_frame = QFrame()
        tablo_frame.setStyleSheet(Styles.get_inner_card_style())
        tablo_layout = QVBoxLayout(tablo_frame)
        
        tablo_baslik = QLabel("Ölçüm Değerleri ve Öneriler")
        tablo_baslik.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        tablo_layout.addWidget(tablo_baslik)
        
        uyari_mesajlari = []
        eksik_olcumler = []
        
        if not sabah_olcumler:
            eksik_olcumler.append("Sabah")
        if not ogle_olcumler:
            eksik_olcumler.append("Öğle")
        if not ikindi_olcumler:
            eksik_olcumler.append("İkindi")
        if not aksam_olcumler:
            eksik_olcumler.append("Akşam")
        if not gece_olcumler:
            eksik_olcumler.append("Gece")
        
        if eksik_olcumler:
            eksik_mesaj = f"Eksik ölçümler: {', '.join(eksik_olcumler)}. Bu ölçümler ortalamaya dahil edilmedi."
            uyari_mesajlari.append(eksik_mesaj)
        
        toplam_olcum = len(sabah_olcumler) + len(ogle_olcumler) + len(ikindi_olcumler) + len(aksam_olcumler) + len(gece_olcumler)
        if toplam_olcum <= 3:
            uyari_mesajlari.append("Yetersiz veri! Ortalama hesaplaması güvenilir değildir.")
        
        if uyari_mesajlari:
            uyari_frame = QFrame()
            uyari_frame.setStyleSheet("background-color: #fff3cd; border-radius: 8px; padding: 10px; border: 1px solid #ffeeba;")
            uyari_layout = QVBoxLayout(uyari_frame)
            
            uyari_icon = QLabel("⚠️")
            uyari_icon.setStyleSheet("font-size: 20px;")
            uyari_layout.addWidget(uyari_icon, alignment=Qt.AlignCenter)
            
            for mesaj in uyari_mesajlari:
                uyari_label = QLabel(mesaj)
                uyari_label.setStyleSheet("color: #856404; font-size: 14px;")
                uyari_label.setWordWrap(True)
                uyari_layout.addWidget(uyari_label)
            
            tablo_layout.addWidget(uyari_frame)
        
        sabah_deger = sabah_olcumler[0] if sabah_olcumler else None
        sabah_ortalama = sabah_deger if sabah_deger else 0
        sabah_insulin = self.insulin_doz_hesapla(sabah_ortalama) if sabah_deger else "Veri yok"
        
        ogle_deger = ogle_olcumler[0] if ogle_olcumler else None
        if sabah_deger and ogle_deger:
            ogle_ortalama = (sabah_deger + ogle_deger) / 2
        elif ogle_deger:
            ogle_ortalama = ogle_deger
        else:
            ogle_ortalama = 0
        ogle_insulin = self.insulin_doz_hesapla(ogle_ortalama) if ogle_ortalama > 0 else "Veri yok"
        
        ikindi_deger = ikindi_olcumler[0] if ikindi_olcumler else None
        ikindi_degerler = [d for d in [sabah_deger, ogle_deger, ikindi_deger] if d is not None]
        ikindi_ortalama = sum(ikindi_degerler) / len(ikindi_degerler) if ikindi_degerler else 0
        ikindi_insulin = self.insulin_doz_hesapla(ikindi_ortalama) if ikindi_ortalama > 0 else "Veri yok"
        
        aksam_deger = aksam_olcumler[0] if aksam_olcumler else None
        aksam_degerler = [d for d in [sabah_deger, ogle_deger, ikindi_deger, aksam_deger] if d is not None]
        aksam_ortalama = sum(aksam_degerler) / len(aksam_degerler) if aksam_degerler else 0
        aksam_insulin = self.insulin_doz_hesapla(aksam_ortalama) if aksam_ortalama > 0 else "Veri yok"
        
        gece_deger = gece_olcumler[0] if gece_olcumler else None
        gece_degerler = [d for d in [sabah_deger, ogle_deger, ikindi_deger, aksam_deger, gece_deger] if d is not None]
        gece_ortalama = sum(gece_degerler) / len(gece_degerler) if gece_degerler else 0
        gece_insulin = self.insulin_doz_hesapla(gece_ortalama) if gece_ortalama > 0 else "Veri yok"
        
        # Genel ortalama ve insülin önerisi
        tum_degerler = [d for d in [sabah_deger, ogle_deger, ikindi_deger, aksam_deger, gece_deger] if d is not None]
        genel_ortalama = sum(tum_degerler) / len(tum_degerler) if tum_degerler else 0
        genel_insulin_oneri = self.insulin_doz_hesapla(genel_ortalama) if genel_ortalama > 0 else "Veri yok"
        
        # İnsülin önerisini veritabanına kaydet
        try:
            if genel_ortalama > 0:
                # İnsülin doz miktarını sayısal değer olarak al
                if "ml" in genel_insulin_oneri:
                    doz_miktari = float(genel_insulin_oneri.split(" ")[0])
                else:
                    doz_miktari = 0
                
                print(f"İnsülin kaydediliyor: Hasta ID={self.secili_hasta_id}, Tarih={tarih}, Ortalama={genel_ortalama}, Doz={doz_miktari}")
                self.db.add_insulin(
                    self.secili_hasta_id,
                    tarih,
                    genel_ortalama,
                    doz_miktari
                )
                print("İnsülin kaydı başarılı")
        except Exception as e:
            print(f"İnsülin kaydedilirken hata: {str(e)}")
        
        tablo_html = f"""
        <style>
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
                color: #333;
            }}
            .warning {{
                color: #e74c3c;
                font-weight: bold;
            }}
            .normal {{
                color: #27ae60;
                font-weight: bold;
            }}
            .high {{
                color: #e67e22;
                font-weight: bold;
            }}
            .very-high {{
                color: #c0392b;
                font-weight: bold;
            }}
        </style>
        <table>
            <tr>
                <th>Zaman</th>
                <th>Ölçüm Değeri</th>
                <th>Ortalama</th>
                <th>İnsülin Önerisi</th>
            </tr>
            <tr>
                <td>Sabah</td>
                <td>{sabah_deger if sabah_deger else 'Veri yok'}</td>
                <td>{round(sabah_ortalama, 1) if sabah_ortalama > 0 else 'Veri yok'}</td>
                <td>{sabah_insulin}</td>
            </tr>
            <tr>
                <td>Öğle</td>
                <td>{ogle_deger if ogle_deger else 'Veri yok'}</td>
                <td>{round(ogle_ortalama, 1) if ogle_ortalama > 0 else 'Veri yok'}</td>
                <td>{ogle_insulin}</td>
            </tr>
            <tr>
                <td>İkindi</td>
                <td>{ikindi_deger if ikindi_deger else 'Veri yok'}</td>
                <td>{round(ikindi_ortalama, 1) if ikindi_ortalama > 0 else 'Veri yok'}</td>
                <td>{ikindi_insulin}</td>
            </tr>
            <tr>
                <td>Akşam</td>
                <td>{aksam_deger if aksam_deger else 'Veri yok'}</td>
                <td>{round(aksam_ortalama, 1) if aksam_ortalama > 0 else 'Veri yok'}</td>
                <td>{aksam_insulin}</td>
            </tr>
            <tr>
                <td>Gece</td>
                <td>{gece_deger if gece_deger else 'Veri yok'}</td>
                <td>{round(gece_ortalama, 1) if gece_ortalama > 0 else 'Veri yok'}</td>
                <td>{gece_insulin}</td>
            </tr>
            <tr style="background-color: #e8f4f8; font-weight: bold;">
                <td>Genel</td>
                <td>-</td>
                <td>{round(genel_ortalama, 1) if genel_ortalama > 0 else 'Veri yok'}</td>
                <td>{genel_insulin_oneri}</td>
            </tr>
        </table>
        """
        
        sonuc_label = QLabel(tablo_html)
        tablo_layout.addWidget(sonuc_label)
        
        # İnsülin doz bilgisi
        bilgi_frame = QFrame()
        bilgi_frame.setStyleSheet("background-color: #d4edda; border-radius: 8px; padding: 10px; border: 1px solid #c3e6cb;")
        bilgi_layout = QVBoxLayout(bilgi_frame)
        
        bilgi_baslik = QLabel("📋 İnsülin Doz Bilgisi")
        bilgi_baslik.setStyleSheet("font-size: 14px; font-weight: bold; color: #155724;")
        bilgi_layout.addWidget(bilgi_baslik)
        
        bilgi_icerik = QLabel("""
        <ul>
            <li>< 70 mg/dL (Hipoglisemi): İnsülin önerilmez</li>
            <li>70–110 mg/dL (Normal): İnsülin önerilmez</li>
            <li>111–150 mg/dL (Orta Yüksek): 1 ml insülin önerilir</li>
            <li>151–200 mg/dL (Yüksek): 2 ml insülin önerilir</li>
            <li>> 200 mg/dL (Çok Yüksek): 3 ml insülin önerilir</li>
        </ul>
        """)
        bilgi_icerik.setStyleSheet("color: #155724; font-size: 13px;")
        bilgi_layout.addWidget(bilgi_icerik)
        
        tablo_layout.addWidget(bilgi_frame)
        
        kapat_btn = QPushButton("Kapat")
        kapat_btn.setStyleSheet(Styles.get_button_style())
        kapat_btn.clicked.connect(dialog.close)
        
        card_layout.addWidget(tablo_frame)
        card_layout.addWidget(kapat_btn, alignment=Qt.AlignCenter)
        
        main_layout.addWidget(main_card)
        dialog.setLayout(main_layout)
        dialog.exec_()
    
    def insulin_doz_hesapla(self, ortalama):
        if ortalama < 70:
            return "Önerilmez (Hipoglisemi)"
        elif ortalama <= 110:
            return "Önerilmez (Normal)"
        elif ortalama <= 150:
            return "1 ml (Orta Yüksek)"
        elif ortalama <= 200:
            return "2 ml (Yüksek)"
        else:
            return "3 ml (Çok Yüksek)"

    def belirti_ekle(self):
        if not self.secili_hasta_id or not self.secili_hasta:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir hasta seçin.")
            return
            
        dialog = QDialog(self)
        dialog.setWindowTitle(f"{self.secili_hasta['ad']} {self.secili_hasta['soyad']} - Belirti Ekle")
        dialog.setMinimumSize(400, 400) 
        
        main_layout = QVBoxLayout(dialog)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        main_card = QFrame()
        main_card.setStyleSheet(Styles.get_modern_card_style())
        card_layout = QVBoxLayout(main_card)
        card_layout.setContentsMargins(15, 15, 15, 15)  
        card_layout.setSpacing(10) 
        
        baslik = QLabel("⚠️ Belirti Ekle")
        baslik.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        card_layout.addWidget(baslik, alignment=Qt.AlignCenter)
        
        hasta_bilgisi = QLabel(f"Hasta: {self.secili_hasta['ad']} {self.secili_hasta['soyad']}")
        hasta_bilgisi.setStyleSheet("font-size: 14px; color: #3498db;")
        card_layout.addWidget(hasta_bilgisi, alignment=Qt.AlignCenter)
        
        belirti_frame = QFrame()
        belirti_frame.setStyleSheet(Styles.get_inner_card_style())
        belirti_layout = QVBoxLayout(belirti_frame)
        
        belirti_baslik = QLabel("Belirti Türü")
        belirti_baslik.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        belirti_layout.addWidget(belirti_baslik)
        
        belirti_turu = QComboBox()
        belirti_turu.addItems([
            "Poliüri (Sık idrara çıkma)",
            "Polifaji (Aşırı açlık hissi)",
            "Polidipsi (Aşırı susama hissi)",
            "Nöropati (El ve ayaklarda karıncalanma veya uyuşma hissi)",
            "Kilo kaybı",
            "Yorgunluk",
            "Yaraların yavaş iyileşmesi",
            "Bulanık görme"
        ])
        belirti_turu.setStyleSheet("""
            QComboBox {
                border: 1px solid #3498db;
                border-radius: 5px;
                padding: 3px;
                background-color: white;
                font-size: 12px;
                min-height: 25px;
            }
        """)
        belirti_layout.addWidget(belirti_turu)
        
        # Tarih seçimi
        tarih_frame = QFrame()
        tarih_frame.setStyleSheet(Styles.get_inner_card_style())
        tarih_layout = QVBoxLayout(tarih_frame)
        
        tarih_baslik = QLabel("Tarih")
        tarih_baslik.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        tarih_layout.addWidget(tarih_baslik)
        
        tarih = QDateEdit()
        tarih.setDate(QDate.currentDate())
        tarih.setCalendarPopup(True)
        tarih.setStyleSheet("""
            QDateEdit {
                border: 1px solid #3498db;
                border-radius: 5px;
                padding: 3px;
                background-color: white;
                font-size: 12px;
                min-height: 25px;
            }
        """)
        tarih_layout.addWidget(tarih)
        
        buton_layout = QHBoxLayout()  
        
        kaydet_btn = QPushButton("Kaydet")
        kaydet_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 13px;
            }
        """)
        
        kaydet_btn.clicked.connect(lambda: self.belirti_kaydet_dialog(
            dialog, 
            self.secili_hasta_id, 
            tarih.date().toPyDate(),
            belirti_turu.currentText()
        ))
        
        iptal_btn = QPushButton("İptal")
        iptal_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 13px;
            }
        """)
        iptal_btn.clicked.connect(dialog.reject)
        
        buton_layout.addWidget(kaydet_btn)
        buton_layout.addWidget(iptal_btn)
        
        # Kartları ana karta ekle
        card_layout.addWidget(belirti_frame)
        card_layout.addWidget(tarih_frame)
        card_layout.addLayout(buton_layout)  
        
        main_layout.addWidget(main_card)
        
        dialog.exec_()
    
    def belirti_kaydet_dialog(self, dialog, hasta_id, tarih, belirti_turu):
        try:
            self.db.add_symptom(
                hasta_id,
                tarih,
                belirti_turu
            )
            QMessageBox.information(self, "Başarılı", "Belirti kaydedildi.")
            dialog.accept()
            
            # Belirtileri görüntülemek için sor
            cevap = QMessageBox.question(
                self, 
                "Belirtiler", 
                "Hastanın tüm belirtilerini görüntülemek ister misiniz?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if cevap == QMessageBox.Yes:
                self.belirtileri_goruntule()
                
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Belirti kaydedilirken bir hata oluştu: {str(e)}")
            
    def belirtileri_goruntule(self):
        if not self.secili_hasta_id:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir hasta seçin.")
            return
        
        belirtiler = self.db.get_patient_symptoms(self.secili_hasta_id)
        
        if not belirtiler:
            QMessageBox.information(self, "Bilgi", "Bu hasta için kaydedilmiş belirti bulunmamaktadır.")
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Hasta Belirtileri")
        dialog.setMinimumSize(600, 400)
        
        layout = QVBoxLayout()
        
        hasta = self.db.get_user_by_id(self.secili_hasta_id)
        if hasta:
            baslik = QLabel(f"{hasta[2]} {hasta[3]} - Belirti Geçmişi")
        else:
            baslik = QLabel("Belirti Geçmişi")
        baslik.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(baslik)
        
        liste = QListWidget()
        liste.setStyleSheet("""
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 14px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
        """)
        
        for belirti in belirtiler:
            tarih = belirti[2].strftime("%d.%m.%Y")
            belirti_turu = belirti[3]
            
            item_text = f"{tarih} - {belirti_turu}"
            liste.addItem(item_text)
        
        layout.addWidget(liste)
        
        buton_layout = QHBoxLayout()
        
        yeni_ekle_btn = QPushButton("Yeni Belirti Ekle")
        yeni_ekle_btn.setStyleSheet(Styles.get_button_style())
        yeni_ekle_btn.clicked.connect(lambda: [dialog.close(), self.belirti_ekle()])
        
        kapat_btn = QPushButton("Kapat")
        kapat_btn.setStyleSheet(Styles.get_button_style())
        kapat_btn.clicked.connect(dialog.close)
        
        buton_layout.addWidget(yeni_ekle_btn)
        buton_layout.addWidget(kapat_btn)
        
        layout.addLayout(buton_layout)
        
        dialog.setLayout(layout)
        dialog.exec_()

    def diyet_egzersiz_oneri_goster(self):
        if not self.secili_hasta_id or not self.secili_hasta:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir hasta seçin.")
            return
            
        try:
            # Son ölçüm bilgisini al
            olcumler = self.db.get_patient_measurements(self.secili_hasta_id)
            if not olcumler:
                QMessageBox.warning(self, "Uyarı", "Bu hasta için ölçüm kaydı bulunamadı!")
                return
                
            son_olcum = olcumler[0]
            son_kan_sekeri = son_olcum[4]  # kan_seker_degeri
            olcum_tarihi = son_olcum[3].date()
            
            # En son belirtileri al
            belirtiler = self.db.get_patient_symptoms(self.secili_hasta_id)
            belirti_adlari = []
            
            if belirtiler:
                for belirti in belirtiler:
                    belirti_adlari.append(belirti[3])  # belirti_turu
            
            diyet, egzersiz = self.diyet_egzersiz_oneri(son_kan_sekeri, belirti_adlari)
            
            dialog = QDialog(self)
            dialog.setWindowTitle("Diyet & Egzersiz Önerisi")
            dialog.setMinimumSize(600, 500)
            
            main_layout = QVBoxLayout()
            
            main_card = QFrame()
            main_card.setStyleSheet(Styles.get_modern_card_style())
            card_layout = QVBoxLayout(main_card)
            
            baslik = QLabel("🍽️ 🏋️ Diyet & Egzersiz Önerisi")
            baslik.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
            card_layout.addWidget(baslik, alignment=Qt.AlignCenter)
            
            hasta_bilgisi = QLabel(f"Hasta: {self.secili_hasta['ad']} {self.secili_hasta['soyad']}")
            hasta_bilgisi.setStyleSheet("font-size: 16px; color: #3498db;")
            card_layout.addWidget(hasta_bilgisi, alignment=Qt.AlignCenter)
            
            olcum_bilgisi = QLabel(f"Son Ölçüm: {son_kan_sekeri} mg/dL ({olcum_tarihi.strftime('%d.%m.%Y')})")
            olcum_bilgisi.setStyleSheet("font-size: 14px; color: #7f8c8d;")
            card_layout.addWidget(olcum_bilgisi, alignment=Qt.AlignCenter)
            
            durum = "Hipoglisemi"
            renk = "#e74c3c"  # kırmızı
            if 70 <= son_kan_sekeri <= 110:
                durum = "Normal - Alt Düzey"
                renk = "#2ecc71"  # yeşil
            elif 110 < son_kan_sekeri < 180:
                durum = "Normal - Üst Düzey / Hafif Yüksek"
                renk = "#f39c12"  # turuncu
            elif son_kan_sekeri >= 180:
                durum = "Hiperglisemi"
                renk = "#e74c3c"  # kırmızı
                
            durum_bilgisi = QLabel(f"Durum: {durum}")
            durum_bilgisi.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {renk};")
            card_layout.addWidget(durum_bilgisi, alignment=Qt.AlignCenter)
            
            if belirti_adlari:
                belirti_frame = QFrame()
                belirti_frame.setStyleSheet(Styles.get_inner_card_style())
                belirti_layout = QVBoxLayout(belirti_frame)
                
                belirti_baslik = QLabel("⚠️ Kaydedilmiş Belirtiler:")
                belirti_baslik.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
                belirti_layout.addWidget(belirti_baslik)
                
                for belirti in belirti_adlari:
                    belirti_label = QLabel(f"• {belirti}")
                    belirti_label.setStyleSheet("font-size: 13px; color: #2c3e50;")
                    belirti_layout.addWidget(belirti_label)
                
                card_layout.addWidget(belirti_frame)
            else:
                belirti_bilgi = QLabel("Kaydedilmiş belirti bulunmamaktadır.")
                belirti_bilgi.setStyleSheet("font-style: italic; color: #7f8c8d;")
                card_layout.addWidget(belirti_bilgi)
            
            oneri_frame = QFrame()
            oneri_frame.setStyleSheet(Styles.get_inner_card_style())
            oneri_layout = QVBoxLayout(oneri_frame)
            
            oneri_baslik = QLabel("📋 Öneriler")
            oneri_baslik.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
            oneri_layout.addWidget(oneri_baslik)
            
            diyet_baslik = QLabel("🍽️ Diyet Önerisi:")
            diyet_baslik.setStyleSheet("font-size: 14px; font-weight: bold; color: #27ae60;")
            oneri_layout.addWidget(diyet_baslik)
            
            diyet_label = QLabel(diyet)
            diyet_label.setStyleSheet("font-size: 14px; color: #2c3e50; margin-left: 10px;")
            oneri_layout.addWidget(diyet_label)
            
            egzersiz_baslik = QLabel("🏋️ Egzersiz Önerisi:")
            egzersiz_baslik.setStyleSheet("font-size: 14px; font-weight: bold; color: #2980b9;")
            oneri_layout.addWidget(egzersiz_baslik)
            
            egzersiz_label = QLabel(egzersiz)
            egzersiz_label.setStyleSheet("font-size: 14px; color: #2c3e50; margin-left: 10px;")
            oneri_layout.addWidget(egzersiz_label)
            
            card_layout.addWidget(oneri_frame)
            
            bilgi_frame = QFrame()
            bilgi_frame.setStyleSheet("background-color: #d4edda; border-radius: 8px; padding: 10px; border: 1px solid #c3e6cb;")
            bilgi_layout = QVBoxLayout(bilgi_frame)
            
            bilgi_baslik = QLabel("ℹ️ Bilgi")
            bilgi_baslik.setStyleSheet("font-size: 14px; font-weight: bold; color: #155724;")
            bilgi_layout.addWidget(bilgi_baslik)
            
            bilgi_icerik = QLabel(
                "Bu öneriler hastanın son ölçüm değerine ve kaydedilen belirtilere göre otomatik olarak oluşturulmuştur. "
                "Tedavi planı için doktor görüşü esastır."
            )
            bilgi_icerik.setStyleSheet("color: #155724; font-size: 13px;")
            bilgi_icerik.setWordWrap(True)
            bilgi_layout.addWidget(bilgi_icerik)
            
            card_layout.addWidget(bilgi_frame)
            
            buton_layout = QHBoxLayout()
            
            diyet_ekle_btn = QPushButton("Diyet Kaydı Ekle")
            diyet_ekle_btn.setStyleSheet(Styles.get_button_style())
            diyet_ekle_btn.clicked.connect(lambda: [dialog.close(), self.diyet_ekle()])
            
            kapat_btn = QPushButton("Kapat")
            kapat_btn.setStyleSheet(Styles.get_button_style())
            kapat_btn.clicked.connect(dialog.close)
            
            buton_layout.addWidget(diyet_ekle_btn)
            buton_layout.addWidget(kapat_btn)
            
            card_layout.addLayout(buton_layout)
            
            main_layout.addWidget(main_card)
            dialog.setLayout(main_layout)
            dialog.exec_()
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Diyet ve egzersiz önerisi oluşturulurken bir hata oluştu:\n{str(e)}")
            
    def diyet_egzersiz_oneri(self, kan_sekeri, belirtiler):
        """
        Kan şekeri seviyesi ve belirtilere göre diyet ve egzersiz önerisi verir.
        Tablodaki kurallara göre otomatik öneri üretir.
        
        Args:
            kan_sekeri: int, hastanın kan şekeri seviyesi (mg/dL)
            belirtiler: list of str, kaydedilmiş hasta belirtileri
            
        Returns:
            tuple: (diyet_onerisi, egzersiz_onerisi)
        """
        # Belirtiler listesini küçük harfe dönüştür
        belirtiler_lower = [b.lower() if b else "" for b in belirtiler]
        
        # < 70 mg/dL (Hipoglisemi)
        if kan_sekeri < 70:
            if any(belirti in b.lower() for b in belirtiler_lower for belirti in ["nöropati", "polifaj", "yorgunluk"]):
                return "Dengeli Beslenme", "Yok"
            return "Dengeli Beslenme", "Yok"  # Varsayılan hipoglisemi önerisi
            
        # 70-110 mg/dL (Normal - Alt Düzey)
        elif 70 <= kan_sekeri <= 110:
            if any(belirti in b.lower() for b in belirtiler_lower for belirti in ["yorgun", "kilo kayb"]):
                return "Az Şekerli Diyet", "Yürüyüş"
            elif any(belirti in b.lower() for b in belirtiler_lower for belirti in ["polifaj", "polidipsi"]):
                return "Dengeli Beslenme", "Yürüyüş"
            return "Dengeli Beslenme", "Yürüyüş"  # Varsayılan normal alt düzey önerisi
            
        # 110-180 mg/dL (Normal - Üst Düzey / Hafif Yüksek)
        elif 110 < kan_sekeri < 180:
            if any(belirti in b.lower() for b in belirtiler_lower for belirti in ["bulanık görme", "nöropati"]):
                return "Az Şekerli Diyet", "Klinik Egzersiz"
            elif any(belirti in b.lower() for b in belirtiler_lower for belirti in ["poliüri", "polidipsi"]):
                return "Şekersiz Diyet", "Klinik Egzersiz"
            elif any(belirti in b.lower() for b in belirtiler_lower for belirti in ["yorgun", "nöropati", "bulanık"]):
                return "Az Şekerli Diyet", "Yürüyüş"
            return "Az Şekerli Diyet", "Yürüyüş"  # Varsayılan normal üst düzey önerisi
            
        # >= 180 mg/dL (Hiperglisemi)
        else:  # kan_sekeri >= 180
            if any(belirti in b.lower() for b in belirtiler_lower for belirti in ["yara", "yavaş", "iyileşme", "polifaj", "polidipsi"]):
                return "Şekersiz Diyet", "Klinik Egzersiz"
            elif any(belirti in b.lower() for b in belirtiler_lower for belirti in ["yara", "yavaş", "iyileşme", "kilo kayb"]):
                return "Şekersiz Diyet", "Yürüyüş"
            return "Şekersiz Diyet", "Yürüyüş"  # Varsayılan hiperglisemi önerisi

    def grafik_goster(self):
        """Hastanın kan şekeri değişimlerinin, diyet ve egzersizlerin etkisinin grafiksel gösterimi"""
        if not self.secili_hasta_id:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir hasta seçin.")
            return
            
        try:
            # Verileri çekelim
            olcumler = self.db.get_patient_measurements(self.secili_hasta_id)
            diyetler = self.db.get_patient_diets(self.secili_hasta_id)
            egzersizler = self.db.get_patient_exercises(self.secili_hasta_id)
            
            if not olcumler:
                QMessageBox.warning(self, "Veri Yok", "Hasta için kan şekeri ölçümü bulunmamaktadır.")
                return
                
            # Verileri düzenleyelim
            tarihler = []
            kan_sekeri_degerleri = []
            zaman_etiketleri = []
            
            # Tarih formatı
            for olcum in olcumler:
                tarih = olcum[3]  # ölçüm tarihi
                deger = olcum[4]  # kan_seker_degeri
                zaman = olcum[5] if olcum[5] else "Belirtilmemiş"  # ölçüm_zamani
                
                tarihler.append(tarih)
                kan_sekeri_degerleri.append(deger)
                zaman_etiketleri.append(zaman)
            
            # Diyetleri düzenle
            diyet_tarihleri = []
            diyet_turleri = []
            diyet_uygulanma = []
            
            for diyet in diyetler:
                diyet_tarihleri.append(diyet[2])  # tarih
                diyet_turleri.append(diyet[3])    # diyet_turu
                diyet_uygulanma.append(diyet[4])  # uygulandı mı (bool)
            
            # Egzersizleri düzenle
            egzersiz_tarihleri = []
            egzersiz_turleri = []
            egzersiz_yapilma = []
            
            for egzersiz in egzersizler:
                egzersiz_tarihleri.append(egzersiz[2])  # tarih
                egzersiz_turleri.append(egzersiz[3])    # egzersiz_turu
                egzersiz_yapilma.append(egzersiz[4])    # yapıldı mı (bool)
            
            # Dialog oluştur
            dialog = QDialog(self)
            dialog.setWindowTitle(f"{self.secili_hasta['ad']} {self.secili_hasta['soyad']} - Grafiksel Analiz")
            dialog.setMinimumSize(1000, 800)
            
            # Ana layout
            main_layout = QVBoxLayout(dialog)
            
            # Başlık
            baslik = QLabel("📈 Kan Şekeri Değişimi ve Etki Analizi")
            baslik.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50; margin-bottom: 15px;")
            main_layout.addWidget(baslik, alignment=Qt.AlignCenter)
            
            # Tarih aralığı seçimi
            tarih_frame = QFrame()
            tarih_frame.setStyleSheet(Styles.get_inner_card_style())
            tarih_layout = QHBoxLayout(tarih_frame)
            
            tarih_layout.addWidget(QLabel("Başlangıç Tarihi:"))
            baslangic_tarihi = QDateEdit()
            if tarihler:
                baslangic_tarihi.setDate(min(tarihler).date())
            else:
                baslangic_tarihi.setDate(QDate.currentDate().addMonths(-1))
            baslangic_tarihi.setCalendarPopup(True)
            tarih_layout.addWidget(baslangic_tarihi)
            
            tarih_layout.addWidget(QLabel("Bitiş Tarihi:"))
            bitis_tarihi = QDateEdit()
            if tarihler:
                bitis_tarihi.setDate(max(tarihler).date())
            else:
                bitis_tarihi.setDate(QDate.currentDate())
            bitis_tarihi.setCalendarPopup(True)
            tarih_layout.addWidget(bitis_tarihi)
            
            filtrele_btn = QPushButton("Filtrele")
            filtrele_btn.setStyleSheet(Styles.get_button_style())
            tarih_layout.addWidget(filtrele_btn)
            
            main_layout.addWidget(tarih_frame)
            
            # Figure ve Canvas hazırla
            figure = Figure(figsize=(10, 8), dpi=100)
            canvas = FigureCanvas(figure)
            main_layout.addWidget(canvas)
            
            # 1. Grafik: Kan Şekeri Değişimi
            ax1 = figure.add_subplot(311)  # 3 satır 1 sütun, 1. grafik
            
            # 2. Grafik: Diyet Türü ve Kan Şekeri İlişkisi
            ax2 = figure.add_subplot(312)  # 3 satır 1 sütun, 2. grafik
            
            # 3. Grafik: Egzersiz ve Kan Şekeri İlişkisi
            ax3 = figure.add_subplot(313)  # 3 satır 1 sütun, 3. grafik
            
            # Grafik çizme fonksiyonu
            def grafikleri_guncelle():
                baslangic = baslangic_tarihi.date().toPyDate()
                bitis = bitis_tarihi.date().toPyDate()
                
                # Her grafiği temizle
                ax1.clear()
                ax2.clear()
                ax3.clear()
                
                # Filtreleme
                filtered_data = [(tarih, deger, zaman) for tarih, deger, zaman in 
                                zip(tarihler, kan_sekeri_degerleri, zaman_etiketleri) 
                                if baslangic <= tarih.date() <= bitis]
                
                if not filtered_data:
                    QMessageBox.warning(dialog, "Veri Yok", "Seçilen tarih aralığında veri bulunamadı.")
                    return
                
                f_tarihler, f_degerler, f_zamanlar = zip(*filtered_data)
                
                # 1. Grafik: Kan Şekeri Değişimi (Zamana göre)
                ax1.plot(f_tarihler, f_degerler, 'o-', color='#3498db', linewidth=2, markersize=6)
                ax1.set_title('Kan Şekeri Değişimi', fontsize=12, fontweight='bold')
                ax1.set_ylabel('Kan Şekeri (mg/dL)', fontsize=10)
                ax1.set_xlabel('Tarih', fontsize=10)
                ax1.grid(True, linestyle='--', alpha=0.7)
                
                # Normal kan şekeri aralığını göster
                ax1.axhspan(70, 110, alpha=0.2, color='green', label='Normal Aralık (70-110 mg/dL)')
                ax1.axhspan(110, 180, alpha=0.2, color='yellow', label='Yüksek Normal (110-180 mg/dL)')
                ax1.axhspan(180, max(f_degerler) + 20, alpha=0.2, color='red', label='Yüksek (>180 mg/dL)')
                ax1.axhspan(0, 70, alpha=0.2, color='orange', label='Düşük (<70 mg/dL)')
                ax1.legend(loc='upper right', fontsize=9)
                
                # Öğün zamanlarını işaretle
                renkler = {'Sabah': 'blue', 'Öğle': 'green', 'İkindi': 'purple', 'Akşam': 'orange', 'Gece': 'red'}
                for tarih, deger, zaman in zip(f_tarihler, f_degerler, f_zamanlar):
                    renk = renkler.get(zaman, 'black')
                    ax1.annotate(zaman, (tarih, deger), textcoords="offset points", 
                                 xytext=(0,10), ha='center', fontsize=8, color=renk)
                
                # 2. Grafik: Diyet Türlerinin Kan Şekerine Etkisi
                diyet_etkileri = {}
                
                # Her diyet türü için ortalama kan şekeri değişimini hesapla
                for diyet_tarih, diyet_tur, uygulandi in zip(diyet_tarihleri, diyet_turleri, diyet_uygulanma):
                    if baslangic <= diyet_tarih <= bitis and uygulandi:
                        # Diyetten sonraki gün ölçümleri
                        sonraki_gun = diyet_tarih + timedelta(days=1)
                        onceki_gun = diyet_tarih - timedelta(days=1)
                        
                        # Diyetten önceki gün ortalama kan şekeri
                        onceki_degerler = [deger for tarih, deger in zip(tarihler, kan_sekeri_degerleri) 
                                          if tarih.date() == onceki_gun]
                        onceki_ortalama = sum(onceki_degerler) / len(onceki_degerler) if onceki_degerler else None
                        
                        # Diyet günü ortalama kan şekeri
                        diyet_gunu_degerler = [deger for tarih, deger in zip(tarihler, kan_sekeri_degerleri) 
                                             if tarih.date() == diyet_tarih]
                        diyet_gunu_ortalama = sum(diyet_gunu_degerler) / len(diyet_gunu_degerler) if diyet_gunu_degerler else None
                        
                        # Diyetten sonraki gün ortalama kan şekeri
                        sonraki_degerler = [deger for tarih, deger in zip(tarihler, kan_sekeri_degerleri) 
                                           if tarih.date() == sonraki_gun]
                        sonraki_ortalama = sum(sonraki_degerler) / len(sonraki_degerler) if sonraki_degerler else None
                        
                        if diyet_tur not in diyet_etkileri:
                            diyet_etkileri[diyet_tur] = {
                                'onceki': [],
                                'diyet_gunu': [],
                                'sonraki': []
                            }
                        
                        if onceki_ortalama:
                            diyet_etkileri[diyet_tur]['onceki'].append(onceki_ortalama)
                        if diyet_gunu_ortalama:
                            diyet_etkileri[diyet_tur]['diyet_gunu'].append(diyet_gunu_ortalama)
                        if sonraki_ortalama:
                            diyet_etkileri[diyet_tur]['sonraki'].append(sonraki_ortalama)
                
                # Diyet türlerinin etkisini çiz
                x = np.arange(3)  # Önceki, Diyet Günü, Sonraki
                width = 0.15
                multiplier = 0
                
                for diyet_tur, veriler in diyet_etkileri.items():
                    if not (veriler['onceki'] or veriler['diyet_gunu'] or veriler['sonraki']):
                        continue
                    
                    ortalamalar = [
                        sum(veriler['onceki']) / len(veriler['onceki']) if veriler['onceki'] else 0,
                        sum(veriler['diyet_gunu']) / len(veriler['diyet_gunu']) if veriler['diyet_gunu'] else 0,
                        sum(veriler['sonraki']) / len(veriler['sonraki']) if veriler['sonraki'] else 0
                    ]
                    
                    offset = width * multiplier
                    rects = ax2.bar(x + offset, ortalamalar, width, label=diyet_tur)
                    ax2.bar_label(rects, padding=3, fontsize=8)
                    multiplier += 1
                
                ax2.set_ylabel('Ortalama Kan Şekeri (mg/dL)', fontsize=10)
                ax2.set_title('Diyet Türlerinin Kan Şekerine Etkisi', fontsize=12, fontweight='bold')
                ax2.set_xticks(x + width * (len(diyet_etkileri) - 1) / 2)
                ax2.set_xticklabels(['Diyetten Önceki Gün', 'Diyet Günü', 'Diyetten Sonraki Gün'])
                ax2.legend(loc='upper right', fontsize=9)
                ax2.grid(True, linestyle='--', axis='y', alpha=0.7)
                
                # 3. Grafik: Egzersiz ve Kan Şekeri İlişkisi
                egzersiz_etkileri = {}
                
                # Her egzersiz türü için ortalama kan şekeri değişimini hesapla
                for egzersiz_tarih, egzersiz_tur, yapildi in zip(egzersiz_tarihleri, egzersiz_turleri, egzersiz_yapilma):
                    if baslangic <= egzersiz_tarih <= bitis and yapildi:
                        # Egzersizden sonraki gün ölçümleri
                        sonraki_gun = egzersiz_tarih + timedelta(days=1)
                        
                        # Egzersiz günü ortalama kan şekeri
                        egzersiz_gunu_degerler = [deger for tarih, deger in zip(tarihler, kan_sekeri_degerleri) 
                                               if tarih.date() == egzersiz_tarih]
                        egzersiz_gunu_ortalama = sum(egzersiz_gunu_degerler) / len(egzersiz_gunu_degerler) if egzersiz_gunu_degerler else None
                        
                        # Egzersizden sonraki gün ortalama kan şekeri
                        sonraki_degerler = [deger for tarih, deger in zip(tarihler, kan_sekeri_degerleri) 
                                           if tarih.date() == sonraki_gun]
                        sonraki_ortalama = sum(sonraki_degerler) / len(sonraki_degerler) if sonraki_degerler else None
                        
                        if egzersiz_tur not in egzersiz_etkileri:
                            egzersiz_etkileri[egzersiz_tur] = {
                                'egzersiz_gunu': [],
                                'sonraki': []
                            }
                        
                        if egzersiz_gunu_ortalama:
                            egzersiz_etkileri[egzersiz_tur]['egzersiz_gunu'].append(egzersiz_gunu_ortalama)
                        if sonraki_ortalama:
                            egzersiz_etkileri[egzersiz_tur]['sonraki'].append(sonraki_ortalama)
                
                # Egzersiz türlerinin etkisini çiz
                x = np.arange(2)  # Egzersiz Günü, Sonraki Gün
                width = 0.15
                multiplier = 0
                
                for egzersiz_tur, veriler in egzersiz_etkileri.items():
                    if not (veriler['egzersiz_gunu'] or veriler['sonraki']):
                        continue
                    
                    ortalamalar = [
                        sum(veriler['egzersiz_gunu']) / len(veriler['egzersiz_gunu']) if veriler['egzersiz_gunu'] else 0,
                        sum(veriler['sonraki']) / len(veriler['sonraki']) if veriler['sonraki'] else 0
                    ]
                    
                    offset = width * multiplier
                    rects = ax3.bar(x + offset, ortalamalar, width, label=egzersiz_tur)
                    ax3.bar_label(rects, padding=3, fontsize=8)
                    multiplier += 1
                
                ax3.set_ylabel('Ortalama Kan Şekeri (mg/dL)', fontsize=10)
                ax3.set_title('Egzersizlerin Kan Şekerine Etkisi', fontsize=12, fontweight='bold')
                ax3.set_xticks(x + width * (len(egzersiz_etkileri) - 1) / 2)
                ax3.set_xticklabels(['Egzersiz Günü', 'Egzersizden Sonraki Gün'])
                ax3.legend(loc='upper right', fontsize=9)
                ax3.grid(True, linestyle='--', axis='y', alpha=0.7)
                
                figure.tight_layout()
                canvas.draw()
            
            # İlk çizimi yap
            grafikleri_guncelle()
            
            # Filtreleme olayını bağla
            filtrele_btn.clicked.connect(grafikleri_guncelle)
            
            # Alt butonlar
            buton_layout = QHBoxLayout()
            
            kapat_btn = QPushButton("Kapat")
            kapat_btn.setStyleSheet(Styles.get_button_style())
            kapat_btn.clicked.connect(dialog.close)
            
            kaydet_btn = QPushButton("Grafikleri Kaydet")
            kaydet_btn.setStyleSheet(Styles.get_button_style())
            
            def grafikleri_kaydet():
                dosya_yolu, _ = QFileDialog.getSaveFileName(
                    dialog, 
                    "Grafikleri Kaydet",
                    f"{self.secili_hasta['ad']}_{self.secili_hasta['soyad']}_kan_sekeri_analizi.png",
                    "PNG Dosyası (*.png);;JPEG Dosyası (*.jpg)"
                )
                if dosya_yolu:
                    figure.savefig(dosya_yolu, dpi=300, bbox_inches='tight')
                    QMessageBox.information(dialog, "Başarılı", f"Grafikler {dosya_yolu} konumuna kaydedildi.")
            
            kaydet_btn.clicked.connect(grafikleri_kaydet)
            
            buton_layout.addWidget(kaydet_btn)
            buton_layout.addWidget(kapat_btn)
            
            main_layout.addLayout(buton_layout)
            
            dialog.exec_()
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Grafikler oluşturulurken bir hata oluştu: {str(e)}")

class HastaEklePenceresi(QWidget): 
    def __init__(self, doktor, db):
        super().__init__()
        self.setWindowTitle("Hasta Ekle")
        self.setGeometry(100,100,400,200)         
        self.doktor = doktor
        self.db = db

        self.tc_no_label = QLabel("TC Kimlik NO")
        self.tc_no = QLineEdit(self)
        self.tc_no.setPlaceholderText("Hasta TC Kimlik NO")

        self.tc_no.setMaxLength(11)
        regex = QRegularExpression("^[0-9]{0,11}$")
        self.tc_no.setValidator(QRegularExpressionValidator(regex))
        self.tc_no.setStyleSheet(Styles.get_input_style())

        self.ad_label = QLabel("Hasta Adı") 
        self.ad = QLineEdit(self)
        self.ad.setPlaceholderText("Hasta adını giriniz.") 
        self.ad.setStyleSheet(Styles.get_input_style())

        self.soyad_label = QLabel("Hasta Soyadı") 
        self.soyad = QLineEdit(self)
        self.soyad.setPlaceholderText("Hasta soyadını giriniz") 
        self.soyad.setStyleSheet(Styles.get_input_style())

        self.cinsiyet_label = QLabel("Hasta Cinsiyeti")
        self.cinsiyet = QComboBox()
        self.cinsiyet.addItems(["Erkek","Kadın"])
        self.cinsiyet.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #2980b9;
                border-radius: 8px;
                background-color: #fdfefe;
                font-size: 14px;
            }
            QComboBox:hover {
                border-color: #1abc9c;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left: 1px solid #2980b9;
            }
            QComboBox::down-arrow {
                image: url(down-arrow.png);
                width: 14px;
                height: 14px;
            }
        """)

        self.dogum_tarihi_label = QLabel("Hasta Doğum Tarihi") 
        self.dogum_tarihi = QLineEdit(self)
        self.dogum_tarihi.setPlaceholderText("Hasta doğum tarihini giriniz. ")
        self.dogum_tarihi.setStyleSheet(Styles.get_input_style())

        self.eposta_label = QLabel("Hasta E-posta adresi")
        self.eposta = QLineEdit(self)
        self.eposta.setPlaceholderText("Hasta epostası giriniz") 
        self.eposta.setStyleSheet(Styles.get_input_style())

        self.sifre_label = QLabel("Hasta Sifre")
        self.sifre = QLineEdit(self)
        self.sifre.setPlaceholderText("Hasta Sifresini giriniz")
        self.sifre.setStyleSheet(Styles.get_input_style())

        self.sifre_tekrar_label = QLabel("Hasta Sifre (Tekrar)")
        self.sifre_tekrar = QLineEdit(self)
        self.sifre_tekrar.setPlaceholderText("Hasta sifresini tekrar giriniz")
        self.sifre_tekrar.setStyleSheet(Styles.get_input_style())

        self.email_gonder_check = QComboBox()
        self.email_gonder_check.addItems(["Evet, email gönder", "Hayır, email gönderme"])
        self.email_gonder_check.setStyleSheet(Styles.get_modern_combobox_style())

        self.kayit_button = QPushButton("Kayıt Oluştur", self)
        self.kayit_button.clicked.connect(self.HastaKayitOlustur)
        self.kayit_button.setStyleSheet(Styles.get_button_style())

        ana_layout = QHBoxLayout()

        foto_hizalama = QHBoxLayout()

        self.foto_label = QLabel("Henüz fotoğraf yok")
        self.foto_label.setFixedSize(120, 120)
        self.foto_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #2980b9;
                border-radius: 10px;
                background-color: #f0f8ff;
                color: #7f8c8d;
                font-size: 12px;
                qproperty-alignment: AlignCenter;
            }
        """)
        self.foto_label.setScaledContents(True)
        self.foto_button = QPushButton("Fotoğraf Seç")
        self.foto_button.clicked.connect(self.foto_sec)
        self.foto_button.setStyleSheet(Styles.get_button_style())

        self.foto_sil_button = QPushButton("❌")
        self.foto_sil_button.setFixedSize(24, 24)
        self.foto_sil_button.setToolTip("Fotoğrafı temizle")
        self.foto_sil_button.clicked.connect(self.foto_temizle)
        self.foto_sil_button.hide()
        
        foto_hizalama.addWidget(self.foto_label)
        foto_hizalama.addWidget(self.foto_sil_button, alignment=Qt.AlignTop)

        foto_layout = QVBoxLayout()
        foto_layout.addLayout(foto_hizalama)  
        foto_layout.addWidget(self.foto_button)

        layout = QVBoxLayout()
        layout.addWidget(self.tc_no_label)
        layout.addWidget(self.tc_no)
        layout.addWidget(self.ad_label)
        layout.addWidget(self.ad)
        layout.addWidget(self.soyad_label)
        layout.addWidget(self.soyad)
        layout.addWidget(self.cinsiyet_label)
        layout.addWidget(self.cinsiyet)
        layout.addWidget(self.dogum_tarihi_label)
        layout.addWidget(self.dogum_tarihi)
        layout.addWidget(self.eposta_label)
        layout.addWidget(self.eposta)
        layout.addWidget(self.sifre_label)
        layout.addWidget(self.sifre)
        layout.addWidget(self.sifre_tekrar_label)
        layout.addWidget(self.sifre_tekrar)
        layout.addWidget(QLabel("Hasta kayıt bilgilerini e-posta ile gönder:"))
        layout.addWidget(self.email_gonder_check)
        layout.addWidget(self.kayit_button)

        ana_layout.addLayout(foto_layout)
        ana_layout.addLayout(layout)
        self.setLayout(ana_layout)

    def formu_temizle(self):
        self.tc_no.clear()
        self.ad.clear()
        self.soyad.clear()
        self.dogum_tarihi.clear()
        self.eposta.clear()
        self.sifre.clear()
        self.sifre_tekrar.clear()
        self.cinsiyet.setCurrentIndex(0)
        self.foto_temizle()

    def email_gonder(self, alici_eposta, ad, soyad, tc_kimlik_no, sifre):
        try:
            if self.email_gonder_check.currentText() == "Hayır, email gönderme":
                return True
                
            # Email oluştur
            mesaj = MIMEMultipart()
            mesaj['From'] = EMAIL_GONDEREN
            mesaj['To'] = alici_eposta
            mesaj['Subject'] = "Diyabet Takip Uygulaması - Hesap Bilgileriniz"
            
            # Email içeriği
            icerik = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; color: #333; }}
                    .container {{ padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
                    h2 {{ color: #3498db; }}
                    .bilgi {{ margin: 10px 0; }}
                    .onemli {{ color: #e74c3c; font-weight: bold; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>Diyabet Takip Uygulaması - Hesap Bilgileriniz</h2>
                    <p>Sayın {ad} {soyad},</p>
                    <p>Diyabet Takip Uygulamasına kaydınız başarıyla oluşturulmuştur. Aşağıda giriş bilgilerinizi bulabilirsiniz:</p>
                    
                    <div class="bilgi">
                        <strong>Kullanıcı Adı (TC Kimlik No):</strong> {tc_kimlik_no}
                    </div>
                    <div class="bilgi">
                        <strong>Şifre:</strong> {sifre}
                    </div>
                    
                    <p class="onemli">Giriş yaptıktan sonra şifrenizi değiştirmenizi öneririz.</p>
                    
                    <p>İyi günler dileriz,<br>
                    Diyabet Takip Uygulaması Ekibi</p>
                </div>
            </body>
            </html>
            """
            
            mesaj.attach(MIMEText(icerik, 'html'))
            
            # SMTP bağlantısı
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30)
            server.starttls()
            
            server.login(EMAIL_GONDEREN, EMAIL_SIFRE)
            server.send_message(mesaj)
            server.quit()
            
            return True
            
        except Exception as e:
            QMessageBox.warning(self, "Email Gönderme Hatası", 
                f"Email gönderilirken bir hata oluştu: {str(e)}\n\n"
                f"Bu hatayı almaya devam ederseniz lütfen uygulama yöneticinize başvurun.")
            return False

    def HastaKayitOlustur(self): 
        tc = self.tc_no.text()
        ad = self.ad.text()
        soyad = self.soyad.text()
        dogum_tarihi = self.dogum_tarihi.text()
        eposta = self.eposta.text()
        sifre = self.sifre.text()
        sifre_tekrar = self.sifre_tekrar.text()
        cinsiyet = self.cinsiyet.currentText()

        if not all([tc, ad, soyad, dogum_tarihi, eposta, sifre, sifre_tekrar, cinsiyet]):
            QMessageBox.warning(self, "Eksik Bilgi", "Lütfen tüm alanları doldurun.")
            return        
        if sifre != sifre_tekrar:
            QMessageBox.warning(self, "Şifreler Eşleşmiyor", "Girdiğiniz şifreler eşleşmiyor. Lütfen kontrol ediniz.")
            return
        if len(tc) != 11:
            QMessageBox.warning(self, "Geçersiz TC Kimlik NO", "TC kimlik NO 11 rakamdan az olamaz.")
            return

        try:
            dogum_tarihi = datetime.strptime(dogum_tarihi, "%d.%m.%Y").date()
        except ValueError:
            QMessageBox.warning(self, "Hatalı Tarih", "Doğum tarihi DD.MM.YYYY formatında olmalı.")
            return        

        sifre_hash = hashlib.sha256(sifre.encode()).hexdigest()
        profil_bytes = None
        if hasattr(self, 'secilen_foto_path') and self.secilen_foto_path:
            with open(self.secilen_foto_path, "rb") as f:
                profil_bytes = f.read()

        try:
            hasta_id = self.db.add_patient(tc, ad, soyad, dogum_tarihi, sifre_hash, cinsiyet, eposta, profil_bytes)
            self.db.add_patient_doctor_relation(self.doktor['id'], hasta_id)
            
            # Email gönderme işlemi
            email_gonderildi = self.email_gonder(eposta, ad, soyad, tc, sifre)
            
            basari_mesaji = "Yeni hasta kaydınız başarıyla yapılmıştır."
            if email_gonderildi and self.email_gonder_check.currentText() == "Evet, email gönder":
                basari_mesaji += " Bilgiler hastanın e-posta adresine gönderildi."
            
            QMessageBox.information(self, "Başarılı", basari_mesaji)
            self.formu_temizle()
            if hasattr(self.parent(), 'hasta_listesine_git'):
                self.parent().hasta_listesine_git()
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Hasta kaydı oluşturulurken bir hata oluştu: {str(e)}")

    def foto_sec(self):
        dosya_path, _ = QFileDialog.getOpenFileName(
            self, "Fotoğraf Seç", "", "Resim Dosyaları (*.png *.jpg *.jpeg)"
        )
        if dosya_path:
            self.secilen_foto_path = dosya_path
            pixmap = QPixmap(dosya_path).scaled(120, 120)
            self.foto_label.setPixmap(pixmap)
            self.foto_sil_button.show()

    def foto_temizle(self):
        self.foto_label.clear()
        self.foto_label.setText("Henüz fotoğraf yok")
        self.secilen_foto_path = None
        self.foto_sil_button.hide()

class DoktorPanel(QWidget):
    def __init__(self, doktor, doktor_id, db):
        super().__init__()
        self.setWindowTitle("Doktor Paneli")
        self.setGeometry(100, 100, 800, 600)
        self.doktor = doktor
        self.doktor_id = doktor_id
        self.db = db

        self.main_layout = QVBoxLayout()
        
        self.label = QLabel(f"Hoş geldiniz Dr. {doktor['ad']} {doktor['soyad']}")
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        
        button_layout = QHBoxLayout()
        
        self.hastaGoruntule = QPushButton("Hastalarımı Görüntüle", self)
        self.hastaGoruntule.setStyleSheet(Styles.get_button_style())
        self.hastaEkleButton = QPushButton("Yeni Hasta Kaydı", self)
        self.hastaEkleButton.setStyleSheet(Styles.get_button_style())
        self.uyarilarButton = QPushButton("⚠️ Uyarılar", self)
        self.uyarilarButton.setStyleSheet(Styles.get_button_style())
        
        self.hastaGoruntule.clicked.connect(self.hasta_listesine_git)
        self.hastaEkleButton.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.uyarilarButton.clicked.connect(self.uyarilari_goster)
        
        button_layout.addWidget(self.hastaGoruntule)
        button_layout.addWidget(self.hastaEkleButton)
        button_layout.addWidget(self.uyarilarButton)

        self.stacked_widget = QStackedWidget()
        
        self.hasta_liste_widget = HastaListePenceresi(self.doktor, self.db)
        self.stacked_widget.addWidget(self.hasta_liste_widget)
        
        self.hasta_ekle_widget = HastaEklePenceresi(self.doktor, self.db)
        self.stacked_widget.addWidget(self.hasta_ekle_widget)
        
        self.main_layout.addWidget(self.label)
        self.main_layout.addLayout(button_layout)
        self.main_layout.addWidget(self.stacked_widget)
        
        self.setLayout(self.main_layout)

    def hasta_listesine_git(self):
        self.hasta_liste_widget.hastalari_getir()  
        self.stacked_widget.setCurrentIndex(0)

    def hasta_listesini_yenile(self):
        self.hasta_liste_widget.hastalari_getir()
        self.stacked_widget.setCurrentIndex(0)

    def uyarilari_goster(self):
        hastalar = self.db.get_doctor_patients(self.doktor_id)
        bugun = datetime.now().date()
        
        for hasta in hastalar:
            hasta_id = hasta[0]
            hasta_adi = f"{hasta[2]} {hasta[3]}"
            
            olcumler = self.db.get_patient_measurements(hasta_id)
            bugun_olcumler = [o for o in olcumler if o[3].date() == bugun]
            
            if not bugun_olcumler:
                self.db.add_alert(
                    hasta_id=hasta_id,
                    uyari_turu="Acil Uyarı !",
                    mesaj=f"{hasta_adi} Hasta gün boyunca kan şekeri ölçümü yapmamıştır. Acil takip önerilir. "
                )
            elif len(bugun_olcumler) < 3:
                self.db.add_alert(
                    hasta_id=hasta_id,
                    uyari_turu="Yetersiz Ölçüm",
                    mesaj=f"{hasta_adi} için Hastanın günlük kan şekeri ölçüm sayısı yetersiz (<3). Durum izlenmelidir. "
                )
            
            for olcum in bugun_olcumler:
                deger = olcum[4]
                if deger < 70:
                    self.db.add_alert(
                        hasta_id=hasta_id,
                        uyari_turu="Acil Uyarı !",
                        mesaj=f"{hasta_adi} için Hastanın kan şekeri seviyesi 70 mg/dL'nin altına düştü. Hipoglisemi riski! Hızlı müdahale gerekebilir. "
                    )
                elif deger > 200:
                    self.db.add_alert(
                        hasta_id=hasta_id,
                        uyari_turu="Acil Müdahale Uyarısı",
                        mesaj=f"{hasta_adi} içinHastanın kan şekeri 200 mg/dL'nin üzerinde. Hiperglisemi durumu. Acil müdahale gerekebilir. "
                    )
                elif deger > 111 and deger <= 150 : 
                    self.db.add_alert(
                        hasta_id = hasta_id,
                        uyari_turu = "Takip Uyarısı" ,
                        mesaj = f"{hasta_adi} Hastanın kan şekeri 111-150 mg/dL arasında. Durum izlenmeli. "
                    )
                elif deger > 150 and deger <= 200 : 
                    self.db.add_alert(
                        hasta_id = hasta_id,
                        uyari_turu = "İzleme Uyarısı" ,
                        mesaj = f"{hasta_adi} Hastanın kan şekeri 151-200 mg/dL arasında. Durum izlenmeli. "
                    )

        dialog = QDialog(self)
        dialog.setWindowTitle("Hasta Uyarıları")
        dialog.setMinimumSize(800, 600)
        
        layout = QVBoxLayout()
        
        baslik = QLabel("⚠️ Hasta Uyarıları")
        baslik.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        layout.addWidget(baslik)
        
        uyari_listesi = QListWidget()
        uyari_listesi.setStyleSheet("""
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 14px;
                padding: 5px;
                background-color: white;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #eee;
                color: #2c3e50;
                background-color: white;
            }
            QListWidget::item:selected {
                background-color: #e8f4f8;
                color: #2c3e50;
            }
            QListWidget::item:hover {
                background-color: #f5f6fa;
            }
        """)
        
        uyarilar = self.db.get_doctor_alerts(self.doktor_id)
        
        if not uyarilar:
            uyari_listesi.addItem("Henüz hiç uyarı bulunmamaktadır.")
        else:
            for uyari in uyarilar:
                hasta_adi = f"{uyari[5]} {uyari[6]}"  # kullanici tablosundan gelen ad ve soyad
                tarih = uyari[2].strftime("%d.%m.%Y %H:%M")
                uyari_turu = uyari[3]
                mesaj = uyari[4]
                
                emoji = "⚠️"
                if "Kritik" in uyari_turu:
                    emoji = "🔴"
                elif "Yetersiz" in uyari_turu:
                    emoji = "🟡"
                elif "Eksik" in uyari_turu:
                    emoji = "🟠"
                
                item_text = f"{emoji} {tarih} - {hasta_adi}\n{uyari_turu}\n📝 {mesaj}"
                uyari_listesi.addItem(item_text)
        
        layout.addWidget(uyari_listesi)
        
        buton_layout = QHBoxLayout()
        
        temizle_btn = QPushButton("Uyarıları Temizle")
        temizle_btn.setStyleSheet(Styles.get_button_style())
        temizle_btn.clicked.connect(lambda: self.uyarilari_temizle(dialog))
        
        kapat_btn = QPushButton("Kapat")
        kapat_btn.setStyleSheet(Styles.get_button_style())
        kapat_btn.clicked.connect(dialog.close)
        
        buton_layout.addWidget(temizle_btn)
        buton_layout.addWidget(kapat_btn)
        
        layout.addLayout(buton_layout)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def uyarilari_temizle(self, dialog):
        cevap = QMessageBox.question(
            self,
            "Uyarıları Temizle",
            "Tüm uyarıları temizlemek istediğinizden emin misiniz?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if cevap == QMessageBox.Yes:
            try:
                hastalar = self.db.get_doctor_patients(self.doktor_id)
                for hasta in hastalar:
                    self.db.clear_patient_alerts(hasta[0])
                QMessageBox.information(self, "Başarılı", "Tüm uyarılar temizlendi.")
                dialog.close()
            except Exception as e:
                QMessageBox.warning(self, "Hata", f"Uyarılar temizlenirken bir hata oluştu: {str(e)}")
