DROP TABLE IF EXISTS Career_History;
DROP TABLE IF EXISTS Alumni;
DROP TABLE IF EXISTS Company;
DROP TABLE IF EXISTS Department;

CREATE TABLE Department (
    department_id INT PRIMARY KEY, 
    department_name VARCHAR(100) NOT NULL 
);

CREATE TABLE Company (
    company_id INT PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    sector VARCHAR(50) NOT NULL
);

CREATE TABLE Alumni (
    alumni_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    contact_info VARCHAR(100),
    graduation_year INT NOT NULL,
    gpa DECIMAL(3,2),
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES Department(department_id) 
);

CREATE TABLE Career_History (
    career_id INT PRIMARY KEY,
    alumni_id INT,
    company_id INT,
    job_title VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE, 
    salary DECIMAL(10,2),
    FOREIGN KEY (alumni_id) REFERENCES Alumni(alumni_id),
    FOREIGN KEY (company_id) REFERENCES Company(company_id)
);

INSERT INTO Department (department_id, department_name) VALUES
(1, 'Data Science'),
(2, 'Computer Engineering'),
(3, 'Industrial Engineering'),
(4, 'Mechanical Engineering'),
(5, 'Business Administration'),
(6, 'Electrical and Electronics Engineering'),
(7, 'Software Engineering');

INSERT INTO Company (company_id, company_name, sector) VALUES
(101, 'TechData A.S.', 'Information Technology'),
(102, 'Garanti Bankasi', 'Finance'),
(103, 'Turkcell', 'Telecommunications'),
(104, 'Aselsan', 'Defense Industry'),
(105, 'Ford Otosan', 'Automotive'),
(106, 'Trendyol', 'E-Commerce'),
(107, 'Turk Hava Yollari', 'Aviation'),
(108, 'Akbank', 'Finance'),
(109, 'Siemens', 'Electronics'),
(110, 'Yemeksepeti', 'E-Commerce');

INSERT INTO Alumni (alumni_id, first_name, last_name, contact_info, graduation_year, gpa, department_id) VALUES
(1, 'Elif', 'Tufek', 'elif@email.com', 2025, 3.80, 1),
(2, 'Ayse', 'Kaya', 'ayse.k@email.com', 2024, 3.20, 2),
(3, 'Mehmet', 'Demir', 'mehmet.d@email.com', 2025, 2.90, 1),
(4, 'Zeynep', 'Celik', 'zeynep.c@email.com', 2023, 3.50, 3),
(5, 'Burak', 'Yilmaz', 'burak.y@email.com', 2021, 3.10, 4),
(6, 'Ceren', 'Ozturk', 'ceren.o@email.com', 2022, 3.65, 5),
(7, 'Deniz', 'Aydin', 'deniz.a@email.com', 2023, 2.80, 2),
(8, 'Emre', 'Ozdemir', 'emre.o@email.com', 2020, 3.40, 6),
(9, 'Fatma', 'Arslan', 'fatma.a@email.com', 2024, 3.90, 7),
(10, 'Gokhan', 'Dogan', 'gokhan.d@email.com', 2021, 2.75, 4),
(11, 'Hakan', 'Kilic', 'hakan.k@email.com', 2022, 3.25, 3),
(12, 'Irem', 'Cetin', 'irem.c@email.com', 2025, 3.85, 1),
(13, 'Kaan', 'Kara', 'kaan.k@email.com', 2023, 3.15, 6),
(14, 'Leyla', 'Koc', 'leyla.k@email.com', 2020, 3.60, 5),
(15, 'Mert', 'Kurt', 'mert.k@email.com', 2024, 2.95, 7),
(16, 'Nur', 'Ozkan', 'nur.o@email.com', 2021, 3.30, 2),
(17, 'Onur', 'Simsek', 'onur.s@email.com', 2025, 3.70, 1),
(18, 'Pelin', 'Polat', 'pelin.p@email.com', 2022, 3.00, 3),
(19, 'Ridvan', 'Oz', 'ridvan.o@email.com', 2023, 3.45, 4),
(20, 'Selin', 'Yildirim', 'selin.y@email.com', 2024, 3.55, 6),
(21, 'Tarik', 'Sahin', 'tarik.s@email.com', 2020, 2.85, 5),
(22, 'Umut', 'Yildiz', 'umut.y@email.com', 2021, 3.75, 7),
(23, 'Volkan', 'Erdogan', 'volkan.e@email.com', 2025, 3.20, 2),
(24, 'Yasin', 'Yavuz', 'yasin.y@email.com', 2022, 3.60, 1),
(25, 'Zehra', 'Gunes', 'zehra.g@email.com', 2023, 3.95, 3),
(26, 'Ahmet', 'Turan', 'ahmet.t@email.com', 2024, 2.70, 4),
(27, 'Berna', 'Keser', 'berna.k@email.com', 2021, 3.10, 6),
(28, 'Cem', 'Bozkurt', 'cem.b@email.com', 2020, 3.80, 5),
(29, 'Didem', 'Yalcin', 'didem.y@email.com', 2025, 3.35, 7),
(30, 'Ege', 'Tekin', 'ege.t@email.com', 2022, 3.50, 2),
(31, 'Furkan', 'Avci', 'furkan.a@email.com', 2023, 3.05, 1),
(32, 'Gizem', 'Tas', 'gizem.t@email.com', 2024, 3.90, 3),
(33, 'Hasan', 'Uyar', 'hasan.u@email.com', 2021, 2.90, 4),
(34, 'Ilker', 'Guler', 'ilker.g@email.com', 2020, 3.40, 6),
(35, 'Buse', 'Kaya', 'buse.k@email.com', 2023, 3.40, 2),
(36, 'Can', 'Ozturk', 'can.o@email.com', 2024, 2.85, 3),
(37, 'Derya', 'Akin', 'derya.a@email.com', 2022, 3.70, 1),
(38, 'Efe', 'Sahin', 'efe.s@email.com', 2025, 3.10, 4),
(39, 'Gamze', 'Celik', 'gamze.c@email.com', 2021, 3.90, 5),
(40, 'Hakan', 'Yilmaz', 'hakan.y@email.com', 2023, 3.25, 6),
(41, 'Ilayda', 'Dogan', 'ilayda.d@email.com', 2024, 3.60, 7),
(42, 'Kamil', 'Koc', 'kamil.k@email.com', 2020, 2.95, 2),
(43, 'Merve', 'Aslan', 'merve.a@email.com', 2025, 3.80, 1),
(44, 'Ozan', 'Turan', 'ozan.t@email.com', 2022, 3.45, 3),
(45, 'Pinar', 'Gunes', 'pinar.g@email.com', 2023, 3.55, 4),
(46, 'Sarp', 'Ersoy', 'sarp.e@email.com', 2021, 3.15, 6),
(47, 'Tugce', 'Aydin', 'tugce.a@email.com', 2024, 3.85, 5),
(48, 'Ugur', 'Polat', 'ugur.p@email.com', 2025, 3.30, 7),
(49, 'Yasemin', 'Kurt', 'yasemin.k@email.com', 2020, 3.75, 1),
(50, 'Zeki', 'Demir', 'zeki.d@email.com', 2022, 2.80, 2);

INSERT INTO Career_History (career_id, alumni_id, company_id, job_title, start_date, end_date, salary) VALUES
(1, 1, 101, 'Data Analyst', '2025-06-01', '2026-01-15', 35000.00),
(2, 1, 102, 'Data Scientist', '2026-02-01', NULL, 55000.00),
(3, 2, 101, 'Software Engineer', '2024-08-01', NULL, 45000.00),
(4, 4, 103, 'Business Analyst', '2023-09-01', NULL, 30000.00),
(5, 5, 105, 'Production Engineer', '2021-07-01', '2024-05-10', 38000.00),
(6, 5, 104, 'R&D Engineer', '2024-06-01', NULL, 52000.00),
(7, 6, 108, 'Finance Specialist', '2022-08-15', NULL, 42000.00),
(8, 7, 106, 'Software Developer', '2023-07-20', '2025-01-10', 48000.00),
(9, 7, 110, 'Backend Engineer', '2025-02-01', NULL, 65000.00),
(10, 8, 109, 'Embedded Systems Engineer', '2020-09-01', NULL, 58000.00),
(11, 9, 101, 'Software Architect', '2024-07-01', NULL, 75000.00),
(12, 10, 105, 'Quality Engineer', '2021-08-01', NULL, 40000.00),
(13, 11, 106, 'Process Improvement Specialist', '2022-09-15', NULL, 46000.00),
(14, 12, 101, 'Data Scientist', '2025-07-01', NULL, 50000.00),
(15, 13, 104, 'Electronic Hardware Engineer', '2023-08-01', NULL, 60000.00),
(16, 14, 102, 'Marketing Specialist', '2020-10-01', '2023-03-15', 32000.00),
(17, 14, 106, 'Marketing Manager', '2023-04-01', NULL, 55000.00),
(18, 15, 110, 'Frontend Developer', '2024-08-01', NULL, 42000.00),
(19, 16, 103, 'Systems Engineer', '2021-07-15', NULL, 47000.00),
(20, 17, 102, 'Risk Analyst', '2025-06-20', NULL, 45000.00),
(21, 18, 107, 'Supply Chain Engineer', '2022-08-01', NULL, 53000.00),
(22, 19, 105, 'Project Engineer', '2023-07-01', NULL, 46000.00),
(23, 20, 109, 'Automation Engineer', '2024-09-01', NULL, 51000.00),
(24, 21, 108, 'Customer Relations Manager', '2020-07-01', '2025-05-01', 35000.00),
(25, 21, 102, 'Branch Manager', '2025-06-01', NULL, 65000.00),
(26, 22, 106, 'Full Stack Software Engineer', '2021-08-01', NULL, 80000.00),
(27, 23, 104, 'Cyber Security Expert', '2025-07-15', NULL, 56000.00),
(28, 24, 101, 'Data Engineer', '2022-08-01', NULL, 62000.00),
(29, 25, 107, 'Operations Manager', '2023-09-01', NULL, 70000.00),
(30, 26, 105, 'Field Engineer', '2024-07-01', NULL, 41000.00),
(31, 27, 103, 'Network Engineer', '2021-09-01', NULL, 54000.00),
(32, 28, 108, 'Investment Specialist', '2020-08-01', NULL, 72000.00),
(33, 29, 101, 'Software Test Specialist', '2025-07-01', NULL, 43000.00),
(34, 30, 104, 'AI Researcher', '2022-08-01', NULL, 68000.00),
(35, 31, 106, 'Data Analyst', '2023-07-01', '2025-08-01', 36000.00),
(36, 31, 110, 'Senior Data Analyst', '2025-09-01', NULL, 58000.00),
(37, 32, 107, 'Strategy Analyst', '2024-07-15', NULL, 49000.00),
(38, 33, 105, 'Product Manager', '2021-08-01', NULL, 63000.00),
(39, 34, 109, 'Project Manager', '2020-07-01', NULL, 85000.00),
(40, 35, 102, 'Software Developer', '2023-08-01', '2025-01-01', 45000.00),
(41, 35, 106, 'Senior Developer', '2025-02-01', NULL, 60000.00),
(42, 36, 105, 'Industrial Analyst', '2024-07-01', NULL, 42000.00),
(43, 37, 101, 'Data Engineer', '2022-09-01', NULL, 65000.00),
(44, 38, 104, 'Mechanical Designer', '2025-08-01', NULL, 48000.00),
(45, 39, 108, 'Financial Advisor', '2021-08-01', '2024-05-01', 50000.00),
(46, 39, 102, 'Finance Manager', '2024-06-01', NULL, 75000.00),
(47, 40, 109, 'Electrical Engineer', '2023-07-15', NULL, 53000.00),
(48, 41, 106, 'Frontend Engineer', '2024-09-01', NULL, 47000.00),
(49, 42, 103, 'Network Support', '2020-08-01', '2023-03-01', 35000.00),
(50, 42, 103, 'Network Admin', '2023-04-01', NULL, 52000.00),
(51, 43, 110, 'Data Scientist', '2025-07-01', NULL, 58000.00),
(52, 44, 105, 'Process Engineer', '2022-08-01', NULL, 46000.00),
(53, 45, 107, 'Logistics Analyst', '2023-09-01', NULL, 49000.00),
(54, 46, 109, 'Hardware Engineer', '2021-07-01', NULL, 55000.00),
(55, 47, 102, 'HR Specialist', '2024-08-01', NULL, 41000.00),
(56, 48, 106, 'Backend Developer', '2025-09-01', NULL, 54000.00),
(57, 49, 101, 'Machine Learning Engineer', '2020-09-01', '2024-01-01', 62000.00),
(58, 49, 104, 'AI Lead', '2024-02-01', NULL, 85000.00),
(59, 50, 103, 'System Administrator', '2022-07-01', NULL, 48000.00);

COMMIT;
