-- 1. BÖLÜM VERİLERİ (Toplam 6 Bölüm)
INSERT INTO Bolum (bolum_adi) VALUES 
('Bilgisayar Mühendisliği'),
('Yazılım Mühendisliği'),
('Endüstri Mühendisliği'),
('İşletme'),
('Veri Bilimi ve Analitiği'),
('Elektrik-Elektronik Mühendisliği');

-- 2. ŞİRKET VERİLERİ (Farklı Sektörlerden 10 Şirket)
INSERT INTO Sirket (sirket_adi, sektor) VALUES 
('Google', 'Teknoloji'),
('Aselsan', 'Savunma Sanayi'),
('Garanti BBVA', 'Finans'),
('Trendyol', 'E-Ticaret'),
('Ford Otosan', 'Otomotiv'),
('Turkcell', 'Telekomünikasyon'),
('KPMG', 'Danışmanlık'),
('Havelsan', 'Savunma Sanayi'),
('Amazon', 'E-Ticaret'),
('Microsoft', 'Teknoloji');

-- 3. MEZUN VERİLERİ (Tam 50 Öğrenci)
-- Mezun ID'leri SQLite tarafından otomatik olarak 1'den 50'ye kadar atanacaktır.
INSERT INTO Mezun (ad, soyad, iletisim_bilgisi, mezuniyet_yili, not_ortalamasi, bolum_id) VALUES 
('Ahmet', 'Yılmaz', 'ahmet.y@email.com', 2018, 3.45, 1),
('Ayşe', 'Demir', 'ayse.d@email.com', 2019, 3.80, 2),
('Mehmet', 'Kaya', 'mehmet.k@email.com', 2020, 2.90, 3),
('Fatma', 'Çelik', 'fatma.c@email.com', 2021, 3.15, 4),
('Mustafa', 'Şahin', 'mustafa.s@email.com', 2019, 3.65, 5),
('Zeynep', 'Öztürk', 'zeynep.o@email.com', 2022, 3.95, 6),
('Ali', 'Yıldırım', 'ali.y@email.com', 2018, 2.75, 1),
('Gül', 'Aydın', 'gul.a@email.com', 2023, 3.20, 2),
('Hasan', 'Erdoğan', 'hasan.e@email.com', 2020, 2.60, 3),
('Emine', 'Arslan', 'emine.a@email.com', 2021, 3.40, 4),
('İbrahim', 'Doğan', 'ibrahim.d@email.com', 2019, 3.10, 5),
('Hatice', 'Kılıç', 'hatice.k@email.com', 2022, 3.85, 6),
('Hüseyin', 'Aslan', 'huseyin.a@email.com', 2020, 3.00, 1),
('Sevgi', 'Gök', 'sevgi.g@email.com', 2021, 3.35, 2),
('İsmail', 'Çetin', 'ismail.c@email.com', 2018, 2.85, 3),
('Merve', 'Koç', 'merve.k@email.com', 2023, 3.70, 4),
('Osman', 'Kurt', 'osman.k@email.com', 2019, 3.45, 5),
('Elif', 'Özdemir', 'elif.o@email.com', 2020, 3.90, 6),
('Can', 'Polat', 'can.p@email.com', 2022, 3.25, 1),
('Aylin', 'Güneş', 'aylin.g@email.com', 2021, 3.60, 2),
('Murat', 'Bulut', 'murat.b@email.com', 2018, 2.95, 3),
('Büşra', 'Yıldız', 'busra.y@email.com', 2020, 3.80, 4),
('Kemal', 'Taş', 'kemal.t@email.com', 2019, 3.15, 5),
('Derya', 'Çakır', 'derya.c@email.com', 2023, 3.55, 6),
('Burak', 'Karaca', 'burak.k@email.com', 2021, 3.05, 1),
('Esra', 'Ateş', 'esra.a@email.com', 2022, 3.40, 2),
('Tarık', 'Gül', 'tarik.g@email.com', 2020, 2.80, 3),
('Sibel', 'Tekin', 'sibel.t@email.com', 2019, 3.75, 4),
('Yusuf', 'Ak', 'yusuf.a@email.com', 2018, 3.30, 5),
('Sinem', 'Kara', 'sinem.k@email.com', 2021, 3.65, 6),
('Eren', 'Avcı', 'eren.a@email.com', 2023, 3.90, 1),
('Tuğba', 'Sarı', 'tugba.s@email.com', 2020, 3.20, 2),
('Ozan', 'Yaman', 'ozan.y@email.com', 2022, 2.90, 3),
('Gizem', 'Can', 'gizem.c@email.com', 2019, 3.85, 4),
('Uğur', 'Mutlu', 'ugur.m@email.com', 2021, 3.45, 5),
('Eda', 'Şen', 'eda.s@email.com', 2018, 3.10, 6),
('Kaan', 'Erol', 'kaan.e@email.com', 2020, 3.50, 1),
('Melis', 'Tunç', 'melis.t@email.com', 2023, 3.95, 2),
('Cem', 'Başar', 'cem.b@email.com', 2019, 2.75, 3),
('Özge', 'Vural', 'ozge.v@email.com', 2022, 3.60, 4),
('Tolga', 'Akın', 'tolga.a@email.com', 2021, 3.35, 5),
('Bahar', 'Turan', 'bahar.t@email.com', 2020, 3.70, 6),
('Deniz', 'Sönmez', 'deniz.s@email.com', 2018, 3.00, 1),
('Ceren', 'Erdem', 'ceren.e@email.com', 2019, 3.80, 2),
('Volkan', 'Korkmaz', 'volkan.k@email.com', 2023, 3.25, 3),
('Aslı', 'Gündüz', 'asli.g@email.com', 2021, 3.55, 4),
('Emre', 'Çoban', 'emre.c@email.com', 2020, 2.95, 5),
('Şeyma', 'Özkan', 'seyma.o@email.com', 2022, 3.90, 6),
('Oğuz', 'Uyar', 'oguz.u@email.com', 2019, 3.15, 1),
('Nihan', 'Süer', 'nihan.s@email.com', 2021, 3.45, 2);

-- 4. KARİYER GEÇMİŞİ VERİLERİ
-- NOT: is_cikis_tarihi NULL ise, kişi hala o şirkette aktif çalışıyor demektir.

-- ÖZEL SENARYO 1: Ahmet Yılmaz (Mezun ID: 1) zaman içinde 3 KEZ iş değiştirmiş.
INSERT INTO Kariyer_Gecmisi (mezun_id, sirket_id, pozisyon, ise_giris_tarihi, isten_cikis_tarihi, maas) VALUES 
(1, 6, 'Junior Yazılım Geliştirici', '2018-08-01', '2020-05-15', 35000),  -- Turkcell'den ayrıldı
(1, 4, 'Yazılım Geliştirici', '2020-06-01', '2022-12-30', 55000),         -- Trendyol'dan ayrıldı
(1, 1, 'Senior Yazılım Mühendisi', '2023-01-15', NULL, 90000);          -- Google'da aktif çalışıyor

-- ÖZEL SENARYO 2: Ayşe Demir (Mezun ID: 2) zaman içinde 2 KEZ iş değiştirmiş.
INSERT INTO Kariyer_Gecmisi (mezun_id, sirket_id, pozisyon, ise_giris_tarihi, isten_cikis_tarihi, maas) VALUES 
(2, 7, 'İş Analisti', '2019-09-01', '2022-03-01', 40000),               -- KPMG'den ayrıldı
(2, 10, 'Yazılım Mimarı', '2022-04-01', NULL, 85000);                   -- Microsoft'ta aktif çalışıyor

-- DİĞER MEZUNLARIN KARİYER VERİLERİ (Çeşitlilik sağlamak için rastgele dağıtıldı)
INSERT INTO Kariyer_Gecmisi (mezun_id, sirket_id, pozisyon, ise_giris_tarihi, isten_cikis_tarihi, maas) VALUES 
(3, 5, 'Üretim Planlama Mühendisi', '2020-08-15', NULL, 48000),         -- Ford Otosan (Aktif)
(4, 3, 'Finans Uzmanı', '2021-07-01', NULL, 42000),                     -- Garanti BBVA (Aktif)
(5, 9, 'Veri Analisti', '2019-10-01', '2023-01-10', 50000),             -- Amazon (İşten Ayrılmış, şu an işsiz)
(6, 2, 'Gömülü Sistemler Mühendisi', '2022-09-01', NULL, 65000),        -- Aselsan (Aktif)
(7, 4, 'Backend Geliştirici', '2019-01-01', NULL, 58000),               -- Trendyol (Aktif)
(8, 1, 'Frontend Geliştirici', '2023-08-01', NULL, 45000),              -- Google (Aktif)
(10, 7, 'Yönetim Danışmanı', '2021-09-15', NULL, 60000),                -- KPMG (Aktif)
(11, 4, 'Veri Bilimcisi', '2020-03-01', NULL, 75000),                   -- Trendyol (Aktif)
(12, 8, 'Sistem Mühendisi', '2022-10-01', NULL, 55000),                 -- Havelsan (Aktif)
(13, 6, 'Ağ Uzmanı', '2021-02-01', NULL, 47000),                        -- Turkcell (Aktif)
(16, 3, 'Kredi Risk Analisti', '2023-09-01', NULL, 38000),              -- Garanti BBVA (Aktif)
(18, 2, 'Elektronik Tasarım Mühendisi', '2021-05-01', NULL, 62000),     -- Aselsan (Aktif)
(22, 10, 'Bulut Sistemleri Mühendisi', '2020-11-01', NULL, 80000),      -- Microsoft (Aktif)
(25, 4, 'Yazılım Test Uzmanı', '2022-01-15', '2023-11-01', 40000),      -- Trendyol (İşten Ayrılmış)
(30, 8, 'Donanım Mühendisi', '2021-08-01', NULL, 54000),                -- Havelsan (Aktif)
(31, 1, 'Yapay Zeka Uzmanı', '2023-07-01', NULL, 95000),                -- Google (Aktif)
(34, 7, 'İnsan Kaynakları Uzmanı', '2020-01-01', NULL, 45000),          -- KPMG (Aktif)
(37, 9, 'DevOps Mühendisi', '2021-06-01', NULL, 82000),                 -- Amazon (Aktif)
(40, 3, 'Finansal Raporlama Uzmanı', '2022-05-01', NULL, 43000),        -- Garanti BBVA (Aktif)
(45, 5, 'Kalite Kontrol Mühendisi', '2023-08-15', NULL, 46000),         -- Ford Otosan (Aktif)
(50, 4, 'Full Stack Geliştirici', '2021-09-01', NULL, 68000);           -- Trendyol (Aktif)