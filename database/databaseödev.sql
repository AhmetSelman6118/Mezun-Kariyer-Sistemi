CREATE TABLE IF NOT EXISTS Department (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Company (
    company_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name VARCHAR(100) NOT NULL,
    industry VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Alumni (
    alumni_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    contact_info VARCHAR(100),
    graduation_year INTEGER NOT NULL,
    gpa DECIMAL(3,2),
    department_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES Department(department_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Career_History (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    alumni_id INTEGER,
    company_id INTEGER,
    job_title VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    salary DECIMAL(10,2),
    FOREIGN KEY (alumni_id) REFERENCES Alumni(alumni_id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES Company(company_id) ON DELETE CASCADE
);

INSERT INTO Department (department_name) VALUES 
('Computer Engineering'),
('Software Engineering'),
('Industrial Engineering'),
('Business Administration'),
('Data Science and Analytics'),
('Electrical-Electronics Engineering');

INSERT INTO Company (company_name, industry) VALUES 
('Google', 'Technology'),
('Aselsan', 'Defense Industry'),
('Garanti BBVA', 'Finance'),
('Trendyol', 'E-Commerce'),
('Ford Otosan', 'Automotive'),
('Turkcell', 'Telecommunications'),
('KPMG', 'Consulting'),
('Havelsan', 'Defense Industry'),
('Amazon', 'E-Commerce'),
('Microsoft', 'Technology');

INSERT INTO Alumni (first_name, last_name, contact_info, graduation_year, gpa, department_id) VALUES 
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
('Nihan', 'Süer', 'nihan.s@email.com', 2021, 3.45, 2),
('Elif', 'Tüfek', 'elif.tufek@email.com', 2025, 3.92, 5); 

INSERT INTO Career_History (alumni_id, company_id, job_title, start_date, end_date, salary) VALUES 
(1, 6, 'Junior Software Developer', '2018-08-01', '2020-05-15', 35000),
(1, 4, 'Software Developer', '2020-06-01', '2022-12-30', 55000),
(1, 1, 'Senior Software Engineer', '2023-01-15', NULL, 90000),
(2, 7, 'Business Analyst', '2019-09-01', '2022-03-01', 40000),
(2, 10, 'Software Architect', '2022-04-01', NULL, 85000),
(3, 5, 'Production Planning Engineer', '2020-08-15', NULL, 48000),
(4, 3, 'Finance Specialist', '2021-07-01', NULL, 42000),
(5, 9, 'Data Analyst', '2019-10-01', '2023-01-10', 50000),
(6, 2, 'Embedded Systems Engineer', '2022-09-01', NULL, 65000),
(7, 4, 'Backend Developer', '2019-01-01', NULL, 58000),
(8, 1, 'Frontend Developer', '2023-08-01', NULL, 45000),
(10, 7, 'Management Consultant', '2021-09-15', NULL, 60000),
(11, 4, 'Data Scientist', '2020-03-01', NULL, 75000),
(12, 8, 'Systems Engineer', '2022-10-01', NULL, 55000),
(13, 6, 'Network Specialist', '2021-02-01', NULL, 47000),
(16, 3, 'Credit Risk Analyst', '2023-09-01', NULL, 38000),
(18, 2, 'Electronic Design Engineer', '2021-05-01', NULL, 62000),
(22, 10, 'Cloud Systems Engineer', '2020-11-01', NULL, 80000),
(25, 4, 'Software Test Specialist', '2022-01-15', '2023-11-01', 40000),
(30, 8, 'Hardware Engineer', '2021-08-01', NULL, 54000),
(31, 1, 'AI Specialist', '2023-07-01', NULL, 95000),
(34, 7, 'HR Specialist', '2020-01-01', NULL, 45000),
(37, 9, 'DevOps Engineer', '2021-06-01', NULL, 82000),
(40, 3, 'Financial Reporting Specialist', '2022-05-01', NULL, 43000),
(45, 5, 'Quality Control Engineer', '2023-08-15', NULL, 46000),
(50, 4, 'Full Stack Developer', '2021-09-01', NULL, 68000),
(51, 1, 'Data Analyst', '2025-06-01', NULL, 78000);
