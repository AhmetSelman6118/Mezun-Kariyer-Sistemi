import sqlite3
import os

# Görseldeki dosya yapısına uygun olarak yolları tanımlıyoruz
DB_PATH = os.path.join("database", "kariyer_sistemi.db")
SCHEMA_PATH = os.path.join("database", "schema.sql")

def get_connection():
    """
    Veritabanı bağlantısını oluşturur ve döndürür.
    Projenin diğer dosyalarından veritabanına erişmek için bu fonksiyon kullanılacak.
    """
    # Veritabanı dosyası belirtilen yolda yoksa SQLite otomatik olarak oluşturur.
    conn = sqlite3.connect(DB_PATH)
    
    # Sütun adlarıyla (dictionary mantığıyla) verilere erişmek için row_factory ayarı yapıyoruz.
    # Bu özellik, raporları ekrana basarken kodumuzu çok temiz tutacak.
    conn.row_factory = sqlite3.Row 
    return conn

def veritabanini_kur():
    """
    schema.sql dosyasını okuyarak veritabanı tablolarını sıfırdan oluşturur.
    """
    # SQL şema dosyasının var olup olmadığını kontrol edelim
    if not os.path.exists(SCHEMA_PATH):
        print(f"Hata: '{SCHEMA_PATH}' dosyası bulunamadı! Lütfen klasör yapınızı kontrol edin.")
        return False

    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # schema.sql dosyasını okuyup içindeki komutları çalıştırıyoruz
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

def test_et():
    """
    Sistemin çalışıp çalışmadığını test eden terminal fonksiyonu.
    """
    print("Veritabanı bağlantısı ve kurulumu test ediliyor...\n" + "-"*40)
    
    # 1. Eğer 'database' klasörü henüz yoksa (git vs. nedeniyle boş gelmişse) oluşturalım
    if not os.path.exists("database"):
        os.makedirs("database")
        print("Bilgi: 'database' klasörü oluşturuldu.")

    # 2. Tabloları kuralım
    basarili = veritabanini_kur()
    
    if basarili:
        # 3. Bağlantıyı test edelim ve veritabanındaki tabloları listeleyelim
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # SQLite'ın sistem tablosundan oluşturduğumuz tabloların isimlerini çekiyoruz
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tablolar = cursor.fetchall()
            
            if tablolar:
                print("Kurulum Başarılı! Veritabanında bulunan tablolar şunlar:")
                for tablo in tablolar:
                    print(f" ➔ {tablo['name']}")
                print("\nHer şey hazır! ✅")
            else:
                print("Bağlantı başarılı ancak veritabanında hiç tablo bulunamadı. ")
                print("Uyarı: 'schema.sql' dosyanızın içinin dolu olduğundan emin olun! ⚠️")
                
            conn.close()
        except sqlite3.Error as e:
            print(f"Bağlantı testi sırasında hata: {e} ❌")
    else:
        print("Veritabanı kurulumu başarısız oldu. ❌")

# Eğer bu dosya doğrudan çalıştırılırsa test fonksiyonu devreye girer
if __name__ == "__main__":
    test_et()