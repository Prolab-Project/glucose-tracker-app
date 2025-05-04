from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QListWidget, QPushButton, QLineEdit, QMessageBox, QComboBox, QFileDialog, QGraphicsPixmapItem, QHBoxLayout, QStackedWidget
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Kullanici, Hasta_doktor, Olcum
from PyQt5.QtGui import QRegularExpressionValidator, QPixmap
from PyQt5.QtCore import QRegularExpression, Qt
from datetime import datetime
import hashlib

class HastaListePenceresi(QWidget) :    
    def __init__(self, doktor_id, session):
        super().__init__()

        self.setWindowTitle("Hastalarım")    
        self.setGeometry(100,100,400,200)
        self.doktor = doktor_id
        self.session = session
        self.hasta_listesi = QListWidget()
        self.hasta_listesi.setFixedWidth(600)
        self.hasta_listesi.setStyleSheet("font-size: 16px; padding: 8px;")
        self.layout = QHBoxLayout()  

        sol_layout = QVBoxLayout()

        self.detay_paneli = QWidget()
        self.detay_layout = QVBoxLayout()
        self.detay_label = QLabel("Hasta bilgileri burada görünecek")
        self.detay_layout.addWidget(self.detay_label)
        self.olcum_ekle_btn = QPushButton("➕ Ölçüm Ekle")
        self.goruntule_btn = QPushButton("📊 Ölçümleri Görüntüle")
        self.guncelle_btn = QPushButton("✏️ Bilgileri Güncelle")

        self.detay_layout.addWidget(self.olcum_ekle_btn)
        self.detay_layout.addWidget(self.goruntule_btn)
        self.detay_layout.addWidget(self.guncelle_btn)

        baslik_label = QLabel("🩺 Hastalarım")
        baslik_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")
        self.detay_label.setStyleSheet("color: black; font-size: 16px;")

        sol_layout.addWidget(baslik_label)
        sol_layout.addWidget(self.hasta_listesi)
        self.detay_paneli.setLayout(self.detay_layout)
        self.layout.addWidget(self.detay_paneli)
        self.layout.addLayout(sol_layout)
        self.setLayout(self.layout)
        self.hastalari_getir()

        self.hasta_listesi.itemDoubleClicked.connect(self.hasta_detaylarini_goster)
    
    def hasta_detaylarini_goster(self, item):
        tc = item.text().split("TC: ")[-1]
        hasta = self.session.query(Kullanici).filter_by(tc_kimlik_no=tc).first()

        if hasta:   
            detay = (
                f"<b>Ad:</b> {hasta.ad}<br>"
                f"<b>Soyad:</b> {hasta.soyad}<br>"
                f"<b>TC:</b> {hasta.tc_kimlik_no}<br>"
                f"<b>Email:</b> {hasta.eposta}<br>"
                f"<b>Doğum Tarihi:</b> {hasta.dogum_tarihi.strftime('%d.%m.%Y')}<br>"
            )
            self.detay_label.setText(detay)

    def hastalari_getir(self):
        self.hasta_listesi.clear()  
        eslesmeler = self.session.query(Hasta_doktor).filter_by(doktor_id=self.doktor.id).all()
        for eslesme in eslesmeler:
            hasta = self.session.query(Kullanici).filter_by(id=eslesme.hasta_id).first()
            if hasta: 
                self.hasta_listesi.addItem(f"{hasta.ad} {hasta.soyad} - TC: {hasta.tc_kimlik_no}")

    def olcum_goruntule(self) : 
        eslesmeler = self.session.query(Olcum).filter_by()       

class HastaEklePenceresi(QWidget): 
    def __init__(self, doktor, session):
        super().__init__()
        self.setWindowTitle("Hasta Ekle")
        self.setGeometry(100,100,400,200)         
        self.doktor = doktor  # doktor nesnesini sınıf değişkeni olarak sakla
        self.session = session

        self.tc_no_label = QLabel("TC Kimlik NO")
        self.tc_no= QLineEdit(self)
        self.tc_no.setPlaceholderText("Hasta TC Kimlik NO")

        self.tc_no.setMaxLength(11)
        regex = QRegularExpression("^[0-9]{0,11}$")
        self.tc_no.setValidator(QRegularExpressionValidator(regex))
        self.tc_no.setStyleSheet(self.get_input_style())

        self.ad_label = QLabel ("Hasta Adı") 
        self.ad = QLineEdit(self)
        self.ad.setPlaceholderText("Hasta adını giriniz.") 
        self.ad.setStyleSheet(self.get_input_style())

        self.soyad_label = QLabel("Hasta Soyadı") 
        self.soyad = QLineEdit(self)
        self.soyad.setPlaceholderText("Hasta soyadını giriniz") 
        self.soyad.setStyleSheet(self.get_input_style())

        self.cinsiyet_label = QLabel("Hasta Cinsiyeti")
        self.cinsiyet= QComboBox()
        self.cinsiyet.addItems(["Erkek","Kadın"]) #baska cinsiyet yoktur
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
                image: url(down-arrow.png);  /* istersen ikon koyarız */
                width: 14px;
                height: 14px;
            }
        """)

        self.dogum_tarihi_label = QLabel("Hasta Doğum Tarihi") 
        self.dogum_tarihi = QLineEdit(self)
        self.dogum_tarihi.setPlaceholderText("Hasta doğum tarihini giriniz. ")
        self.dogum_tarihi.setStyleSheet(self.get_input_style())

        self.eposta_label= QLabel("Hasta E-posta adresi")
        self.eposta= QLineEdit(self)
        self.eposta.setPlaceholderText("Hasta epostası giriniz") 
        self.eposta.setStyleSheet(self.get_input_style())

        self.sifre_label = QLabel("Hasta Sifre")
        self.sifre = QLineEdit(self)
        self.sifre.setPlaceholderText("Hasta Sifresini giriniz")
        self.sifre.setStyleSheet(self.get_input_style())

        self.sifre_tekrar_label = QLabel("Hasta Sifre (Tekrar)")
        self.sifre_tekrar = QLineEdit(self)
        self.sifre_tekrar.setPlaceholderText("Hasta sifresini tekrar giriniz")
        self.sifre_tekrar.setStyleSheet(self.get_input_style())

        self.kayit_button = QPushButton("Kayıt Oluştur",self)
        self.kayit_button.clicked.connect(self.HastaKayitOlustur)
        self.kayit_button.setStyleSheet(self.get_button_style())

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
        self.foto_button.setStyleSheet(self.get_button_style())

        self.foto_sil_button = QPushButton("❌")
        self.foto_sil_button.setFixedSize(24, 24)
        self.foto_sil_button.setToolTip("Fotoğrafı temizle")
        self.foto_sil_button.clicked.connect(self.foto_temizle)
        self.foto_sil_button.hide()
        
        # aynı satıra ekle
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

    def HastaKayitOlustur(self): 
        tc=self.tc_no.text()
        ad= self.ad.text()
        soyad = self.soyad.text()
        dogum_tarihi = self.dogum_tarihi.text()
        eposta= self.eposta.text()
        sifre = self.sifre.text()
        sifre_tekrar =self.sifre_tekrar.text()
        cinsiyet = self.cinsiyet.currentText()

        if not all([tc, ad, soyad, dogum_tarihi, eposta, sifre, sifre_tekrar,cinsiyet, ]):
            QMessageBox.warning(self, "Eksik Bilgi", "Lütfen tüm alanları doldurun.")
            return        
        if sifre != sifre_tekrar  : 
            QMessageBox.warning(self, "Şifreler Eşleşmiyor", "Girdiğiniz şifreler eşleşmiyor. Lütfen kontrol ediniz.")
            return
        if (len(tc)!=11) : 
            QMessageBox.warning(self,"Geçersiz TC Kimlik NO", "TC kimlik NO 11 rakamdan az olamaz.")
            return

        mevcut = self.session.query(Kullanici).filter_by(tc_kimlik_no=tc).first()
        if mevcut : 
            QMessageBox.warning(self, "Zaten var", "Bu TC'ye sahip hasta zaten sisteme kayıtlı.")
            return
        
        try:
            dogum_tarihi = datetime.strptime(dogum_tarihi, "%d.%m.%Y").date()
        except ValueError:
            QMessageBox.warning(self, "Hatalı Tarih", "Doğum tarihi DD.MM.YYYY formatında olmalı.")
            return        

        sifre_hash = hashlib.sha256(sifre.encode()).hexdigest()
        yeni_hasta= Kullanici  (
            tc_kimlik_no = tc,
            ad=ad, 
            soyad= soyad,
            dogum_tarihi = dogum_tarihi,
            sifre_hash= sifre_hash,
            eposta=eposta,
            cinsiyet=cinsiyet,
            rol= 'hasta',
            profil_resmi = None
        )
        self.session.add(yeni_hasta)
        self.session.commit()

        eslesme = Hasta_doktor(
            doktor_id= self.doktor.id,
            hasta_id = yeni_hasta.id
        )
        self.session.add(eslesme)
        self.session.commit()

        QMessageBox.information(self, "Başarılı", "Yeni hasta kaydınız başarıyla yapılmıştır.")
        self.formu_temizle()
        if hasattr(self.parent(), 'hasta_listesine_git'):
            self.parent().hasta_listesine_git()

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
                    
class DoktorPanel(QWidget):
    def __init__(self, doktor, doktor_id, session):
        super().__init__()
        self.setWindowTitle("Doktor Paneli")
        self.setGeometry(100, 100, 800, 600)
        self.doktor = doktor
        self.doktor_id = doktor_id
        self.session = session

      
        self.main_layout = QVBoxLayout()
        
      
        self.label = QLabel(f"Hoş geldiniz Dr. {doktor.ad} {doktor.soyad}")
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        
       
        button_layout = QHBoxLayout()
        
        self.hastaGoruntule = QPushButton("Hastalarımı Görüntüle", self)
        self.hastaEkleButton = QPushButton("Yeni Hasta Kaydı", self)
        
        self.hastaGoruntule.clicked.connect(self.hasta_listesine_git)
        self.hastaEkleButton.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        
        button_layout.addWidget(self.hastaGoruntule)
        button_layout.addWidget(self.hastaEkleButton)

       
        self.stacked_widget = QStackedWidget()
        
       
        self.hasta_liste_widget = HastaListePenceresi(self.doktor, self.session)
        self.stacked_widget.addWidget(self.hasta_liste_widget)
        
       
        self.hasta_ekle_widget = HastaEklePenceresi(self.doktor, self.session)
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

