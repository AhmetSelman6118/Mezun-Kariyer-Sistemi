import streamlit as st
import pandas as pd
import pyodbc
import time

# ==========================================
# SAYFA AYARLARI VE ÖZEL TASARIM (CSS)
# ==========================================
st.set_page_config(page_title="ATÜ Mezun Bilgi Sistemi", page_icon="🎓", layout="wide")

custom_css = """
<style>
    .st-emotion-cache-1r6slb0, .st-emotion-cache-1v0mbdj {
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05);
        border: 1px solid #f1f5f9;
        padding: 15px;
    }
    .header-box {
        background-color: #a91b1b; 
        padding: 30px;
        border-radius: 8px;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    .card-title { font-size: 16px; font-weight: bold; color: #1e293b; margin-bottom: 5px; }
    .num-green { color: #2ecc71; font-size: 36px; font-weight: bold; }
    .num-blue { color: #3498db; font-size: 36px; font-weight: bold; }
    .num-purple { color: #9b59b6; font-size: 36px; font-weight: bold; }
    .login-btn { display: block; width: 100%; text-align: center; padding: 10px; border: 1px solid #cbd5e1; border-radius: 5px; color: #334155; text-decoration: none; margin-top: 10px; font-weight: bold;}
    .login-btn:hover { background-color: #f8fafc; }
    .list-item { font-size: 13px; padding: 10px 0; border-bottom: 1px solid #f1f5f9; display: flex; justify-content: space-between; align-items: center;}
    .list-date { color: #64748b; font-size: 11px; white-space: nowrap; margin-left: 10px;}
    .empty-state { color: #94a3b8; font-size: 13px; text-align: center; padding: 20px; font-style: italic;}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# GİRİŞ SİSTEMİ (SESSION STATE)
# ==========================================
# Rol bazlı sistemi yönetmek için state'leri güncelliyoruz
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['role'] = None         # 'admin' veya 'alumni' olacak
    st.session_state['alumni_id'] = None    # Mezun giriş yaparsa ID'sini tutacak
    st.session_state['alumni_name'] = None  # Mezun giriş yaparsa Ad-Soyad tutacak

# ==========================================
# VERİTABANI BAĞLANTI VE VERİ İŞLEMLERİ
# ==========================================
def connect_db():
    try:
        SERVER = 'localhost,1995' 
        DATABASE = 'MezunKariyerSistemi'
        USERNAME = 'sa' 
        PASSWORD = 'adana123'
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={SERVER};'
            f'DATABASE={DATABASE};'
            f'UID={USERNAME};'
            f'PWD={PASSWORD};'
            f'TrustServerCertificate=yes;' 
        )
        return conn
    except Exception as e:
        st.error(f"Veritabanına bağlanılamadı: {e}")
        return None

# Güvenli parametreli sorgu için get_data fonksiyonu güncellendi
def get_data(query, params=()):
    conn = connect_db()
    if conn is None: return pd.DataFrame()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    df = pd.DataFrame([tuple(row) for row in rows], columns=columns)
    for col in df.columns:
        if df[col].dtype == 'object':
            try: df[col] = df[col].astype(float)
            except (ValueError, TypeError): pass
    return df

def execute_query(query, params=()):
    conn = connect_db()
    if conn is None: 
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit() 
        return True
    except Exception as e:
        st.error(f"Veritabanı işlemi sırasında hata oluştu: {e}")
        return False

# ==========================================
# GİRİŞ EKRANI FONKSİYONU
# ==========================================
def login_screen():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/2936/2936769.png", width=100)
        st.title("ATÜ Bilgi Sistemi Girişi")
        
        tab1, tab2 = st.tabs(["🛡️ Yönetici Girişi", "🎓 Mezun Girişi"])
        
        # --- YÖNETİCİ GİRİŞİ ---
        with tab1:
            with st.form("admin_login"):
                user = st.text_input("Kullanıcı Adı")
                password = st.text_input("Şifre", type="password")
                submit_admin = st.form_submit_button("Yönetici Olarak Giriş Yap")
                if submit_admin:
                    if user == "admin" and password == "admin":
                        st.session_state['logged_in'] = True
                        st.session_state['role'] = 'admin'
                        st.rerun()
                    else:
                        st.error("Hatalı yönetici kullanıcı adı veya şifre!")
                        
        # --- MEZUN GİRİŞİ ---
        with tab2:
            with st.form("alumni_login"):
                st.info("Sisteme giriş yapmak için Mezun ID numaranızı ve Adınızı giriniz. (Örn: ID: 51, Ad: Ahmet)")
                a_id_input = st.text_input("Mezun ID Numaranız")
                a_name_input = st.text_input("Adınız (Sadece Ad)")
                submit_alumni = st.form_submit_button("Mezun Olarak Giriş Yap")
                
                if submit_alumni:
                    if a_id_input and a_name_input:
                        try:
                            # ID'yi sayıya çevir
                            alumni_id_int = int(a_id_input)
                            # Veritabanında eşleşme ara
                            check_query = "SELECT alumni_id, first_name, last_name FROM Alumni WHERE alumni_id = ? AND first_name = ?"
                            check_df = get_data(check_query, (alumni_id_int, a_name_input))
                            
                            if not check_df.empty:
                                st.session_state['logged_in'] = True
                                st.session_state['role'] = 'alumni'
                                st.session_state['alumni_id'] = alumni_id_int
                                st.session_state['alumni_name'] = f"{check_df['first_name'].iloc[0]} {check_df['last_name'].iloc[0]}"
                                st.rerun()
                            else:
                                st.error("Sistemde bu ID ve Ad ile eşleşen bir kayıt bulunamadı.")
                        except ValueError:
                            st.error("Mezun ID sadece sayılardan oluşmalıdır!")
                    else:
                        st.warning("Lütfen tüm alanları doldurun.")

# ==========================================
# ANA UYGULAMA DÖNGÜSÜ
# ==========================================
if not st.session_state['logged_in']:
    login_screen()
else:
    # ARAYÜZ (SIDEBAR - YAN MENÜ) DİNAMİK OLARAK OLUŞTURULUYOR
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2936/2936769.png", width=100)
    
    if st.session_state['role'] == 'admin':
        st.sidebar.title("👨‍💼 Yönetici Menüsü")
        menu = [
            "🏠 Ana Sayfa",
            "📊 1. Bölüm Bazlı Mezun Sayısı",
            "🏢 2. Sektör Bazlı İstihdam",
            "💰 3. Bölüm Bazlı Ortalama Maaş",
            "🔄 4. İş Değiştirme Oranı",
            "📈 5. Yıllara Göre İstihdam",
            "📋 6. Mezun Verileri",
            "💼 7. Mezun Kariyer Geçmişi",
            "✏️ 8. Veri Ekle / Güncelle"
        ]
    else:
        # MEZUN MENÜSÜ
        st.sidebar.title(f"🎓 Hoş Geldin,\n{st.session_state['alumni_name']}")
        menu = [
            "🏠 Ana Sayfa",
            "👤 Profilim ve Kariyerim"
        ]

    secim = st.sidebar.radio("Sayfalar", menu)
    st.sidebar.markdown("---")
    st.sidebar.info("📌 **Proje:** Mezun ve Kariyer Takip Sistemi")
    
    if st.sidebar.button("🚪 Güvenli Çıkış"):
        # Çıkış yaparken tüm verileri sıfırla
        st.session_state['logged_in'] = False
        st.session_state['role'] = None
        st.session_state['alumni_id'] = None
        st.session_state['alumni_name'] = None
        st.rerun()

    # ==========================================
    # 🏠 ANA SAYFA (HERKESE AÇIK)
    # ==========================================
    if secim == "🏠 Ana Sayfa":
        df_alumni = get_data("SELECT COUNT(*) AS cnt FROM Alumni")
        toplam_mezun = int(df_alumni['cnt'].iloc[0]) if not df_alumni.empty else 0
        df_active = get_data("SELECT COUNT(DISTINCT alumni_id) AS cnt FROM Career_History WHERE end_date IS NULL")
        aktif_calisan = int(df_active['cnt'].iloc[0]) if not df_active.empty else 0
        df_company = get_data("SELECT COUNT(*) AS cnt FROM Company")
        toplam_sirket = int(df_company['cnt'].iloc[0]) if not df_company.empty else 0

        st.markdown("""
            <div class="header-box">
                <div style="display: flex; align-items: center;">
                    <div style="background: white; border-radius: 50%; width: 60px; height: 60px; display: flex; justify-content: center; align-items: center;">
                        <span style="color: #a91b1b; font-weight: bold; font-size: 20px;">ATÜ</span>
                    </div>
                    <div style="margin-left: 20px;">
                        <h2 style="margin:0; color: white; font-size: 22px;">Adana Alparslan Türkeş Bilim ve Teknoloji Üniversitesi</h2>
                        <p style="margin:0; color: #f8fafc; font-size: 16px;">Mezun Bilgi Sistemi Dashboard</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        # Yönetici portalı butonu görsel amaçlı
        with col1: st.markdown('<div style="background:white; padding:20px; border-radius:10px; border:1px solid #eee; height:140px;"><div class="card-title">🚀 Durum</div><br><h3 style="color:#1e293b; margin:0;">Sistem Aktif</h3></div>', unsafe_allow_html=True)
        with col2: st.markdown(f'<div style="background:white; padding:20px; border-radius:10px; border:1px solid #eee; height:140px;"><div class="card-title">🎓 Toplam Mezun</div><div class="num-blue">{toplam_mezun}</div></div>', unsafe_allow_html=True)
        with col3: st.markdown(f'<div style="background:white; padding:20px; border-radius:10px; border:1px solid #eee; height:140px;"><div class="card-title">⚙️ Aktif Çalışan</div><div class="num-green">{aktif_calisan}</div></div>', unsafe_allow_html=True)
        with col4: st.markdown(f'<div style="background:white; padding:20px; border-radius:10px; border:1px solid #eee; height:140px;"><div class="card-title">🏢 Kayıtlı Şirket</div><div class="num-purple">{toplam_sirket}</div></div>', unsafe_allow_html=True)

        st.write("")
        d_col1, d_col2, d_col3 = st.columns(3)
        with d_col1:
            st.markdown("""
                <div style="background:white; padding:20px; border-radius:10px; border:1px solid #eee; min-height:280px;">
                    <h3 style="margin-top:0; border-bottom:2px solid #a91b1b; padding-bottom:5px;">📢 ATÜ Duyurular</h3>
                    <div class="list-item"><span>ATÜ Kariyer Günleri Etkinliği</span><span class="list-date">10.05.2026</span></div>
                    <div class="list-item"><span>Mezuniyet Töreni Bilgilendirmesi</span><span class="list-date">15.06.2026</span></div>
                    <div class="list-item"><span>TÜBİTAK Proje Başvuruları Başladı</span><span class="list-date">20.04.2026</span></div>
                </div>
            """, unsafe_allow_html=True)
        with d_col2:
            st.markdown("""
                <div style="background-white; padding:20px; border-radius:10px; border:1px solid #eee; min-height:280px;">
                    <h3 style="margin-top:0; border-bottom:2px solid #a91b1b; padding-bottom:5px;">📰 Haberler</h3>
                    <div class="empty-state">Şu an için güncel haber bulunmamaktadır.</div>
                </div>
            """, unsafe_allow_html=True)
        with d_col3:
            st.markdown("""
                <div style="background:white; padding:20px; border-radius:10px; border:1px solid #eee; min-height:280px;">
                    <h3 style="margin-top:0; border-bottom:2px solid #a91b1b; padding-bottom:5px;">📅 Etkinlikler</h3>
                    <div class="list-item"><span>Teknoloji Zirvesi 2026</span><span class="list-date">12.07.2026</span></div>
                    <div class="empty-state">Planlanan etkinlik bulunmamaktadır.</div>
                </div>
            """, unsafe_allow_html=True)

    # ==========================================
    # 👤 SADECE MEZUNLARA ÖZEL: PROFİL SAYFASI
    # ==========================================
    elif secim == "👤 Profilim ve Kariyerim":
        st.subheader(f"👤 {st.session_state['alumni_name']} - Detaylı Profil")
        mevcut_id = st.session_state['alumni_id']
        
        # Mezunun kendi bilgilerini çek
        kisi_sql = """
            SELECT a.contact_info, a.graduation_year, a.gpa, d.department_name 
            FROM Alumni a LEFT JOIN Department d ON a.department_id = d.department_id 
            WHERE a.alumni_id = ?
        """
        kisi_df = get_data(kisi_sql, (mevcut_id,))
        
        if not kisi_df.empty:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Bölüm", str(kisi_df['department_name'].iloc[0]))
            c2.metric("Mezuniyet Yılı", str(int(kisi_df['graduation_year'].iloc[0])))
            c3.metric("GNO", str(kisi_df['gpa'].iloc[0]))
            c4.metric("İletişim", str(kisi_df['contact_info'].iloc[0]))
            
        st.markdown("---")
        st.subheader("💼 Kariyer Geçmişim")
        
        kariyer_sql = """
            SELECT ch.job_title AS [Pozisyon], c.company_name AS [Şirket], c.sector AS [Sektör], 
                   ch.start_date AS [Giriş Tarihi], ch.end_date AS [Ayrılma Tarihi], ch.salary AS [Maaş (TL)]
            FROM Career_History ch INNER JOIN Company c ON ch.company_id = c.company_id
            WHERE ch.alumni_id = ? ORDER BY ch.start_date DESC
        """
        kariyer_df = get_data(kariyer_sql, (mevcut_id,))
        
        if not kariyer_df.empty:
            st.dataframe(kariyer_df, use_container_width=True)
        else:
            st.info("Sistemde kayıtlı bir iş/kariyer geçmişiniz bulunmamaktadır.")

    # ==========================================
    # 🔒 SADECE YÖNETİCİYE ÖZEL SAYFALAR (AŞAĞISI)
    # ==========================================
    elif st.session_state['role'] == 'admin':
        
        if secim == "📊 1. Bölüm Bazlı Mezun Sayısı":
            st.subheader("📊 Bölüm Bazlı Toplam Mezun Sayısı")
            sql = "SELECT d.department_name, COUNT(a.alumni_id) AS total_alumni_count FROM Department d LEFT JOIN Alumni a ON d.department_id = a.department_id GROUP BY d.department_name;"
            df = get_data(sql)
            c1, c2 = st.columns(2)
            with c1: st.dataframe(df, use_container_width=True)
            with c2: st.bar_chart(data=df, x="department_name", y="total_alumni_count", color="#a91b1b")

        elif secim == "🏢 2. Sektör Bazlı İstihdam":
            st.subheader("🏢 Sektör Bazlı İstihdam Dağılımı")
            sql = "SELECT c.sector, COUNT(ch.career_id) AS employee_count FROM Career_History ch INNER JOIN Company c ON ch.company_id = c.company_id GROUP BY c.sector;"
            df = get_data(sql)
            c1, c2 = st.columns(2)
            with c1: st.dataframe(df, use_container_width=True)
            with c2: st.bar_chart(data=df, x="sector", y="employee_count", color="#a91b1b")

        elif secim == "💰 3. Bölüm Bazlı Ortalama Maaş":
            st.subheader("💰 Bölümlere Göre Ortalama Maaş Analizi")
            sql = "SELECT d.department_name, AVG(ch.salary) AS average_salary FROM Department d INNER JOIN Alumni a ON d.department_id = a.department_id INNER JOIN Career_History ch ON a.alumni_id = ch.alumni_id GROUP BY d.department_name;"
            df = get_data(sql)
            c1, c2 = st.columns(2)
            with c1: st.dataframe(df, use_container_width=True)
            with c2: st.bar_chart(data=df, x="department_name", y="average_salary", color="#a91b1b")

        elif secim == "🔄 4. İş Değiştirme Oranı":
            st.subheader("🔄 Ortalama İş Değiştirme Oranı")
            sql = "SELECT (COUNT(ch.career_id) * 1.0) / COUNT(DISTINCT ch.alumni_id) AS turnover_rate FROM Career_History ch;"
            df = get_data(sql)
            oran = df['turnover_rate'].iloc[0] if not df.empty else 0
            st.metric(label="Mezun Başına Düşen Ortalama İş Sayısı", value=f"{oran:.2f}")
            st.dataframe(df, use_container_width=True)

        elif secim == "📈 5. Yıllara Göre İstihdam":
            st.subheader("📈 Mezuniyet Yılına Göre İstihdam Oranı (%)")
            sql = "SELECT a.graduation_year, ((COUNT(DISTINCT CASE WHEN ch.end_date IS NULL THEN ch.alumni_id END) * 1.0) / NULLIF(COUNT(DISTINCT a.alumni_id), 0)) * 100 AS emp_rate FROM Alumni a LEFT JOIN Career_History ch ON a.alumni_id = ch.alumni_id GROUP BY a.graduation_year ORDER BY a.graduation_year"
            df = get_data(sql)
            if not df.empty:
                df['graduation_year'] = df['graduation_year'].astype(str)
                c1, c2 = st.columns(2)
                with c1: st.dataframe(df, use_container_width=True)
                with c2: st.line_chart(data=df, x="graduation_year", y="emp_rate", color="#a91b1b")

        elif secim == "📋 6. Mezun Verileri":
            st.subheader("📋 Tüm Mezun Kayıtları")
            alumni_all_sql = """
                SELECT a.first_name + ' ' + a.last_name AS [Ad Soyad], a.contact_info AS [İletişim], 
                       a.graduation_year AS [Mezuniyet Yılı], a.gpa AS [GNO], d.department_name AS [Bölüm]
                FROM Alumni a LEFT JOIN Department d ON a.department_id = d.department_id
                ORDER BY a.graduation_year DESC
            """
            all_df = get_data(alumni_all_sql)
            if not all_df.empty:
                st.dataframe(all_df, use_container_width=True, height=500)
                csv = all_df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(label="📥 Listeyi CSV Olarak İndir", data=csv, file_name='atu_mezun_listesi.csv', mime='text/csv')

        elif secim == "💼 7. Mezun Kariyer Geçmişi":
            st.subheader("💼 Mezun Kariyer Yolculuğu Analizi")
            alumni_list_df = get_data("SELECT alumni_id, first_name + ' ' + last_name AS full_name FROM Alumni ORDER BY first_name")
            if not alumni_list_df.empty:
                selected_name = st.selectbox("Lütfen İncelemek İstediğiniz Mezunu Seçin:", alumni_list_df['full_name'])
                selected_id = alumni_list_df[alumni_list_df['full_name'] == selected_name]['alumni_id'].values[0]
                history_sql = f"""
                    SELECT ch.job_title AS [Pozisyon], c.company_name AS [Şirket], c.sector AS [Sektör], 
                           ch.start_date AS [Giriş Tarihi], ch.end_date AS [Ayrılma Tarihi], ch.salary AS [Maaş (TL)]
                    FROM Career_History ch INNER JOIN Company c ON ch.company_id = c.company_id
                    WHERE ch.alumni_id = {selected_id} ORDER BY ch.start_date DESC
                """
                history_df = get_data(history_sql)
                if not history_df.empty:
                    st.success(f"**{selected_name}** adlı mezun için toplam **{len(history_df)}** iş kaydı bulundu.")
                    st.dataframe(history_df, use_container_width=True)

        elif secim == "✏️ 8. Veri Ekle / Güncelle":
            st.subheader("✏️ Veri Ekleme ve Güncelleme İşlemleri")
            tab1, tab2 = st.tabs(["➕ Yeni Mezun Ekle", "🔄 Mezun Bilgisi Güncelle"])
            
            with tab1:
                st.markdown("#### Yeni Mezun Kaydı Oluştur")
                dept_df = get_data("SELECT department_id, department_name FROM Department")
                dept_dict = dict(zip(dept_df['department_name'], dept_df['department_id'])) if not dept_df.empty else {}
                
                with st.form("add_alumni_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        f_name = st.text_input("Ad")
                        contact = st.text_input("İletişim Bilgisi (E-posta/Tel)")
                        gpa = st.number_input("Genel Not Ortalaması (GNO)", min_value=0.0, max_value=4.0, step=0.01)
                    with col2:
                        l_name = st.text_input("Soyad")
                        grad_year = st.number_input("Mezuniyet Yılı", min_value=1950, max_value=2050, step=1, value=2024)
                        selected_dept = st.selectbox("Bölüm", options=list(dept_dict.keys()))
                    
                    submit_add = st.form_submit_button("Sisteme Ekle")
                    if submit_add:
                        if f_name and l_name and selected_dept:
                            dept_id = dept_dict[selected_dept]
                            max_id_df = get_data("SELECT ISNULL(MAX(alumni_id), 0) AS max_id FROM Alumni")
                            new_alumni_id = int(max_id_df['max_id'].iloc[0]) + 1
                            
                            query = "INSERT INTO Alumni (alumni_id, first_name, last_name, contact_info, graduation_year, gpa, department_id) VALUES (?, ?, ?, ?, ?, ?, ?)"
                            params = (new_alumni_id, f_name, l_name, contact, grad_year, gpa, dept_id)
                            
                            if execute_query(query, params):
                                st.success(f"{f_name} {l_name} sisteme başarıyla eklendi! Tablo güncelleniyor...")
                                time.sleep(1.5)
                                st.rerun()
                        else:
                            st.warning("Lütfen zorunlu alanları (Ad, Soyad, Bölüm) doldurun.")

            with tab2:
                st.markdown("#### Mevcut Mezun Bilgilerini Güncelle")
                alumni_df = get_data("SELECT alumni_id, first_name + ' ' + last_name AS full_name FROM Alumni ORDER BY first_name")
                
                if not alumni_df.empty:
                    selected_alumni = st.selectbox("Güncellenecek Mezunu Seçin:", alumni_df['full_name'])
                    selected_alumni_id = int(alumni_df[alumni_df['full_name'] == selected_alumni]['alumni_id'].iloc[0])
                    
                    current_data = get_data(f"SELECT contact_info, gpa FROM Alumni WHERE alumni_id = {selected_alumni_id}")
                    curr_contact = current_data['contact_info'].iloc[0] if current_data['contact_info'].iloc[0] else ""
                    curr_gpa = float(current_data['gpa'].iloc[0]) if pd.notna(current_data['gpa'].iloc[0]) else 0.0
                    
                    with st.form("update_alumni_form"):
                        new_contact = st.text_input("Yeni İletişim Bilgisi", value=curr_contact)
                        new_gpa = st.number_input("Yeni GNO", min_value=0.0, max_value=4.0, step=0.01, value=curr_gpa)
                        submit_update = st.form_submit_button("Bilgileri Güncelle")
                        
                        if submit_update:
                            query = "UPDATE Alumni SET contact_info = ?, gpa = ? WHERE alumni_id = ?"
                            params = (new_contact, new_gpa, selected_alumni_id)
                            if execute_query(query, params):
                                st.success("Mezun bilgileri başarıyla güncellendi! Tablo güncelleniyor...")
                                time.sleep(1.5)
                                st.rerun()
                else:
                    st.info("Sistemde güncellenecek mezun kaydı bulunamadı.")
