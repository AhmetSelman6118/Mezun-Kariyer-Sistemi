import streamlit as st
import pandas as pd
import pyodbc

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
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def login_screen():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/2936/2936769.png", width=120)
        st.title("ATÜ Yönetici Girişi")
        with st.form("login_form"):
            user = st.text_input("Kullanıcı Adı")
            password = st.text_input("Şifre", type="password")
            submit = st.form_submit_button("Sisteme Giriş Yap")
            
            if submit:
                if user == "admin" and password == "admin":
                    st.session_state['logged_in'] = True
                    st.rerun()
                else:
                    st.error("Hatalı kullanıcı adı veya şifre!")

# ==========================================
# VERİTABANI VE VERİ ÇEKME
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

def get_data(query):
    conn = connect_db()
    if conn is None:
        return pd.DataFrame()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    data = [tuple(row) for row in rows]
    df = pd.DataFrame(data, columns=columns)
    
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = df[col].astype(float)
            except (ValueError, TypeError): # BURAYA TypeError EKLENDİ, ARTIK TARİHLERDE ÇÖKMEYECEK
                pass
    return df

# ==========================================
# ANA UYGULAMA DÖNGÜSÜ
# ==========================================
if not st.session_state['logged_in']:
    login_screen()
else:
    # ARAYÜZ (SIDEBAR - YAN MENÜ)
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2936/2936769.png", width=100)
    st.sidebar.title("ATÜ Menü")

    menu = [
        "🏠 Ana Sayfa",
        "🔍 Mezun Kariyer Geçmişi",  # YENİ EKLENEN KISIM
        "📊 1. Bölüm Bazlı Mezun Sayısı",
        "🏢 2. Sektör Bazlı İstihdam",
        "💰 3. Bölüm Bazlı Ortalama Maaş",
        "🔄 4. İş Değiştirme Oranı",
        "📈 5. Yıllara Göre İstihdam"
    ]

    secim = st.sidebar.radio("Sayfalar", menu)

    st.sidebar.markdown("---")
    st.sidebar.info("📌 **Proje:** Mezun ve Kariyer Takip Sistemi")
    
    if st.sidebar.button("🚪 Güvenli Çıkış"):
        st.session_state['logged_in'] = False
        st.rerun()

    # ==========================================
    # ANA SAYFA TASARIMI
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
                        <p style="margin:0; color: #f8fafc; font-size: 16px;">Mezun Bilgi Sistemi</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
                <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; height: 140px;">
                    <div class="card-title">🚪 Mezunlar Portalına</div><br>
                    <a href="#" class="login-btn">Giriş Yap</a>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; height: 140px;">
                    <div class="card-title">🎓 Toplam Mezun Kaydı</div>
                    <div class="num-blue">{toplam_mezun}</div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; height: 140px;">
                    <div class="card-title">⚙️ Aktif Çalışan Mezun</div>
                    <div class="num-green">{aktif_calisan}</div>
                </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
                <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; height: 140px;">
                    <div class="card-title">🏢 Kayıtlı Şirket / Kurum</div>
                    <div class="num-purple">{toplam_sirket}</div>
                </div>
            """, unsafe_allow_html=True)

    # ==========================================
    # YENİ SAYFA: MEZUN KARİYER GEÇMİŞİ (TARİHÇE)
    # ==========================================
    elif secim == "🔍 Mezun Kariyer Geçmişi":
        st.subheader("🔍 Mezun Kariyer Yolculuğu Analizi")
        st.write("Bir mezun seçerek tüm iş değişikliklerini kronolojik olarak inceleyebilirsiniz.")
        
        # Tüm mezunları isim-soyisim olarak çek
        alumni_list_df = get_data("SELECT alumni_id, first_name + ' ' + last_name AS full_name FROM Alumni ORDER BY first_name")
        
        if not alumni_list_df.empty:
            selected_name = st.selectbox("Lütfen İncelemek İstediğiniz Mezunu Seçin:", alumni_list_df['full_name'])
            
            # Seçilen ismin ID'sini bul
            selected_id = alumni_list_df[alumni_list_df['full_name'] == selected_name]['alumni_id'].values[0]
            
            # Seçilen mezunun tüm iş geçmişini getir (INNER JOIN ile şirket bilgilerini de alıyoruz)
            history_sql = f"""
                SELECT ch.job_title AS [Pozisyon], 
                       c.company_name AS [Şirket], 
                       c.sector AS [Sektör], 
                       ch.start_date AS [Giriş Tarihi], 
                       ch.end_date AS [Ayrılma Tarihi], 
                       ch.salary AS [Maaş]
                FROM Career_History ch
                INNER JOIN Company c ON ch.company_id = c.company_id
                WHERE ch.alumni_id = {selected_id}
                ORDER BY ch.start_date DESC
            """
            history_df = get_data(history_sql)
            
            if not history_df.empty:
                st.success(f"**{selected_name}** için toplam **{len(history_df)}** iş kaydı bulundu.")
                st.dataframe(history_df, use_container_width=True)
                
                # Küçük bir metrik paneli daha
                col_a, col_b = st.columns(2)
                with col_a:
                    st.info(f"📍 İlk İşe Giriş: {history_df['Giriş Tarihi'].min()}")
                with col_b:
                    st.warning(f"💼 Toplam Deneyim Sayısı: {len(history_df)}")
            else:
                st.warning("Bu mezun için henüz bir kariyer kaydı girilmemiştir.")

    # ==========================================
    # DİĞER RAPOR SAYFALARI (AYNI KALDI)
    # ==========================================
    elif secim == "📊 1. Bölüm Bazlı Mezun Sayısı":
        st.subheader("📊 Bölüm Bazlı Toplam Mezun Sayısı")
        sql = "SELECT d.department_name, COUNT(a.alumni_id) AS total_alumni_count FROM Department d LEFT JOIN Alumni a ON d.department_id = a.department_id GROUP BY d.department_name;"
        df = get_data(sql)
        st.bar_chart(data=df, x="department_name", y="total_alumni_count", color="#a91b1b")

    elif secim == "🏢 2. Sektör Bazlı İstihdam":
        st.subheader("🏢 Sektör Bazlı İstihdam Dağılımı")
        sql = "SELECT c.sector, COUNT(ch.career_id) AS employee_count FROM Career_History ch INNER JOIN Company c ON ch.company_id = c.company_id GROUP BY c.sector;"
        df = get_data(sql)
        st.bar_chart(data=df, x="sector", y="employee_count", color="#a91b1b")

    elif secim == "💰 3. Bölüm Bazlı Ortalama Maaş":
        st.subheader("💰 Bölümlere Göre Ortalama Maaş Analizi")
        sql = "SELECT d.department_name, AVG(ch.salary) AS average_salary FROM Department d INNER JOIN Alumni a ON d.department_id = a.department_id INNER JOIN Career_History ch ON a.alumni_id = ch.alumni_id GROUP BY d.department_name;"
        df = get_data(sql)
        st.bar_chart(data=df, x="department_name", y="average_salary", color="#a91b1b")

    elif secim == "🔄 4. İş Değiştirme Oranı":
        st.subheader("🔄 Ortalama İş Değiştirme Oranı")
        sql = "SELECT (COUNT(ch.career_id) * 1.0) / COUNT(DISTINCT ch.alumni_id) AS average_job_turnover_rate FROM Career_History ch;"
        df = get_data(sql)
        oran = df['average_job_turnover_rate'].iloc[0] if not df.empty else 0
        st.metric(label="Mezun Başına Düşen Ortalama İş Sayısı", value=f"{oran:.2f}")

    elif secim == "📈 5. Yıllara Göre İstihdam":
        st.subheader("📈 Mezuniyet Yılına Göre İstihdam Oranı (%)")
        sql = """
        SELECT a.graduation_year, 
        ((COUNT(DISTINCT CASE WHEN ch.end_date IS NULL THEN ch.alumni_id END) * 1.0) / 
        NULLIF(COUNT(DISTINCT a.alumni_id), 0)) * 100 AS employment_rate_percentage
        FROM Alumni a LEFT JOIN Career_History ch ON a.alumni_id = ch.alumni_id
        GROUP BY a.graduation_year 
        ORDER BY a.graduation_year;
        """
        df = get_data(sql)
        if not df.empty:
            df['graduation_year'] = df['graduation_year'].astype(str)
            st.line_chart(data=df, x="graduation_year", y="employment_rate_percentage", color="#a91b1b")
