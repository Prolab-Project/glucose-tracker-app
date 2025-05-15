from models import create_tables
from db_manager import DatabaseManager
from datetime import date

def main():
    print("Veritabanı tabloları kontrol ediliyor...")
    create_tables()
    
    print("Veritabanı tabloları başarıyla oluşturuldu.")
    print("Program sonlandırılıyor...")

if __name__ == "__main__":
    main()