-- 1. Bölüm Tablosu
-- Projede "Bölüm bazlı analizler" istendiği için bağımsız bir tablo.
CREATE TABLE IF NOT EXISTS Bolum (
    bolum_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bolum_adi VARCHAR(100) NOT NULL
);

--
-- 2. Şirket Tablosu
-- "Sektör bazlı dağılım" raporu için sektör bilgisini içeren bağımsız tablo.
CREATE TABLE IF NOT EXISTS Sirket (
    sirket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sirket_adi VARCHAR(100) NOT NULL,
    sektor VARCHAR(50) NOT NULL
);

-- 3. Mezun Tablosu
-- Mezunun değişmeyen kişisel ve akademik bilgilerini tutar.
CREATE TABLE IF NOT EXISTS Mezun (
    mezun_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad VARCHAR(50) NOT NULL,
    soyad VARCHAR(50) NOT NULL,
    iletisim_bilgisi VARCHAR(100),
    mezuniyet_yili INTEGER NOT NULL,
    not_ortalamasi DECIMAL(3,2),
    bolum_id INTEGER,
    FOREIGN KEY (bolum_id) REFERENCES Bolum(bolum_id) ON DELETE SET NULL
);

-- 4. Kariyer Geçmişi Tablosu
-- Projenin en önemli kısmı: Bir mezunun geçmişe dönük tüm iş değişikliklerini tutar.
CREATE TABLE IF NOT EXISTS Kariyer_Gecmisi (
    kariyer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mezun_id INTEGER,
    sirket_id INTEGER,
    pozisyon VARCHAR(100) NOT NULL,
    ise_giris_tarihi DATE NOT NULL,
    isten_cikis_tarihi DATE, -- NULL ise mezun o şirkette hala çalışıyor demektir
    maas DECIMAL(10,2), -- "Ortalama maaş analizi" için sayısal format
    FOREIGN KEY (mezun_id) REFERENCES Mezun(mezun_id) ON DELETE CASCADE,
    FOREIGN KEY (sirket_id) REFERENCES Sirket(sirket_id) ON DELETE CASCADE
);