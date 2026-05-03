import sqlite3
import os

# Görseldeki dosya yapısına uygun olarak yolları tanımlıyoruz
DB_PATH = os.path.join("database", "kariyer_sistemi.db")
SCHEMA_PATH = os.path.join("database", "schema.sql")
SEED_PATH = os.path.join("database", "seed_data.sql") # YENİ EKLENDİ

def get_connection():
    """
    Veritabanı bağlantısını oluşturur ve döndürür.
    Projenin diğer dosyalarından veritabanına erişmek için bu fonksiyon kullanılacak.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row 
    return conn

def veritabanini_kur():
    """
    schema.sql dosyasını okuyarak veritabanı tablolarını sıfırdan oluşturur.
    """
    if not os.path.exists(SCHEMA_PATH):
        print(f"Hata: '{SCHEMA_PATH}' dosyası bulunamadı! Lütfen klasör yapınızı kontrol edin.")
        return False

    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
            sql_script = file.read()
            
        cursor.executescript(sql_script)
        conn.commit()
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"SQL şeması çalıştırılırken bir veritabanı hatası meydana geldi: {e}")
        return False
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")
        return False

def ornek_verileri_yukle():
    """
    seed_data.sql dosyasını okuyarak test verilerini veritabanına ekler.
    Çift veri girişini (duplicate) önlemek için önce tablonun doluluğunu kontrol eder.
    """
    if not os.path.exists(SEED_PATH):
        print(f"Hata: '{SEED_PATH}' dosyası bulunamadı!")
        return False

    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Veri tekrarını önlemek için Bolum tablosunda kayıt var mı bakıyoruz
        cursor.execute("SELECT COUNT(*) FROM Bolum")
        kayit_sayisi = cursor.fetchone()[0]
        
        if kayit_sayisi > 0:
            print("Bilgi: Veritabanında zaten veriler mevcut, örnek veri yüklemesi atlandı.")
            conn.close()
            return True

        # Eğer tablo boşsa seed_data.sql dosyasını okuyup çalıştır
        with open(SEED_PATH, "r", encoding="utf-8") as file:
            sql_script = file.read()
            
        cursor.executescript(sql_script)
        conn.commit()
        conn.close()
        print("Örnek veriler veritabanına başarıyla yüklendi! 📊")
        return True
        
    except sqlite3.Error as e:
        print(f"Veri yüklenirken bir veritabanı hatası meydana geldi: {e}")
        return False
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")
        return False

def test_et():
    """
    Sistemin çalışıp çalışmadığını test eden terminal fonksiyonu.
    """
    print("Veritabanı bağlantısı ve kurulumu test ediliyor...\n" + "-"*40)
    
    if not os.path.exists("database"):
        os.makedirs("database")
        print("Bilgi: 'database' klasörü oluşturuldu.")

    # 1. Tabloları kur
    kurulum_basarili = veritabanini_kur()
    
    if kurulum_basarili:
        # 2. Örnek verileri yükle
        veri_yukleme_basarili = ornek_verileri_yukle()
        
        if veri_yukleme_basarili:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tablolar = cursor.fetchall()
                
                if tablolar:
                    print("\nKurulum Başarılı! Veritabanında bulunan tablolar şunlar:")
                    for tablo in tablolar:
                        # Her tablodaki kayıt sayısını da ekrana yazdıralım ki verilerin geldiğini görelim
                        cursor.execute(f"SELECT COUNT(*) FROM {tablo['name']}")
                        sayi = cursor.fetchone()[0]
                        
                        # sqlite_sequence tablosu SQLite'ın kendi iç tablosudur, onu gizleyebiliriz
                        if tablo['name'] != 'sqlite_sequence':
                            print(f" ➔ {tablo['name']} ({sayi} kayıt var)")
                            
                    print("\nHer şey hazır! ✅")
                else:
                    print("Bağlantı başarılı ancak veritabanında hiç tablo bulunamadı. ⚠️")
                    
                conn.close()
            except sqlite3.Error as e:
                print(f"Bağlantı testi sırasında hata: {e} ❌")
        else:
            print("Örnek veri yüklemesi başarısız oldu. ❌")
    else:
        print("Veritabanı kurulumu başarısız oldu. ❌")

if __name__ == "__main__":
    test_et()