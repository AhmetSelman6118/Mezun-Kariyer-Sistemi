import streamlit as st
import pandas as pd
import sqlite3
import os

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
        db_path = os.path.join("database", "kariyer_sistemi.db")
        conn = sqlite3.connect(db_path)
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
    columns = [desc[0] for desc in cursor.description]
    data = [tuple(row) for row in rows]
    df = pd.DataFrame(data, columns=columns)
    
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = df[col].astype(float)
            except (ValueError, TypeError): # BURAYA TypeError EKLENDİ, ARTIK TARİHLERDE ÇÖKMEYECEK
                pass
    conn.close()
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
        "📈 5. Yıllara Göre İstihdam",
        "🎓 6. Mezun Verileri"
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
        df_alumni = get_data("SELECT COUNT(*) AS cnt FROM Mezun")
        toplam_mezun = int(df_alumni['cnt'].iloc[0]) if not df_alumni.empty else 0
        
        df_active = get_data("SELECT COUNT(DISTINCT mezun_id) AS cnt FROM Kariyer_Gecmisi WHERE isten_cikis_tarihi IS NULL")
        aktif_calisan = int(df_active['cnt'].iloc[0]) if not df_active.empty else 0
        
        df_company = get_data("SELECT COUNT(*) AS cnt FROM Sirket")
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
        alumni_list_df = get_data("SELECT mezun_id, ad || ' ' || soyad AS full_name FROM Mezun ORDER BY ad")
        
        if not alumni_list_df.empty:
            selected_name = st.selectbox("Lütfen İncelemek İstediğiniz Mezunu Seçin:", alumni_list_df['full_name'])
            
            # Seçilen ismin ID'sini bul
            selected_id = alumni_list_df[alumni_list_df['full_name'] == selected_name]['mezun_id'].values[0]
            
            # Seçilen mezunun tüm iş geçmişini getir (INNER JOIN ile şirket bilgilerini de alıyoruz)
            history_sql = f"""
                SELECT kg.pozisyon AS [Pozisyon], 
                       s.sirket_adi AS [Şirket], 
                       s.sektor AS [Sektör], 
                       kg.ise_giris_tarihi AS [Giriş Tarihi], 
                       kg.isten_cikis_tarihi AS [Ayrılma Tarihi], 
                       kg.maas AS [Maaş]
                FROM Kariyer_Gecmisi kg
                INNER JOIN Sirket s ON kg.sirket_id = s.sirket_id
                WHERE kg.mezun_id = {selected_id}
                ORDER BY kg.ise_giris_tarihi DESC
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
        sql = "SELECT b.bolum_adi, COUNT(m.mezun_id) AS total_alumni_count FROM Bolum b LEFT JOIN Mezun m ON b.bolum_id = m.bolum_id GROUP BY b.bolum_adi;"
        df = get_data(sql)
        st.bar_chart(data=df, x="bolum_adi", y="total_alumni_count", color="#a91b1b")

    elif secim == "🏢 2. Sektör Bazlı İstihdam":
        st.subheader("🏢 Sektör Bazlı İstihdam Dağılımı")
        sql = "SELECT s.sektor, COUNT(kg.kariyer_id) AS employee_count FROM Kariyer_Gecmisi kg INNER JOIN Sirket s ON kg.sirket_id = s.sirket_id GROUP BY s.sektor;"
        df = get_data(sql)
        st.bar_chart(data=df, x="sektor", y="employee_count", color="#a91b1b")

    elif secim == "💰 3. Bölüm Bazlı Ortalama Maaş":
        st.subheader("💰 Bölümlere Göre Ortalama Maaş Analizi")
        sql = "SELECT b.bolum_adi, AVG(kg.maas) AS average_salary FROM Bolum b INNER JOIN Mezun m ON b.bolum_id = m.bolum_id INNER JOIN Kariyer_Gecmisi kg ON m.mezun_id = kg.mezun_id GROUP BY b.bolum_adi;"
        df = get_data(sql)
        st.bar_chart(data=df, x="bolum_adi", y="average_salary", color="#a91b1b")

    elif secim == "🔄 4. İş Değiştirme Oranı":
        st.subheader("🔄 Ortalama İş Değiştirme Oranı")
        sql = "SELECT (COUNT(kg.kariyer_id) * 1.0) / COUNT(DISTINCT kg.mezun_id) AS average_job_turnover_rate FROM Kariyer_Gecmisi kg;"
        df = get_data(sql)
        oran = df['average_job_turnover_rate'].iloc[0] if not df.empty else 0
        st.metric(label="Mezun Başına Düşen Ortalama İş Sayısı", value=f"{oran:.2f}")

    elif secim == "📈 5. Yıllara Göre İstihdam":
        st.subheader("📈 Mezuniyet Yılına Göre İstihdam Oranı (%)")
        sql = """
        SELECT m.mezuniyet_yili, 
        ((COUNT(DISTINCT CASE WHEN kg.isten_cikis_tarihi IS NULL THEN kg.mezun_id END) * 1.0) / 
        NULLIF(COUNT(DISTINCT m.mezun_id), 0)) * 100 AS employment_rate_percentage
        FROM Mezun m LEFT JOIN Kariyer_Gecmisi kg ON m.mezun_id = kg.mezun_id
        GROUP BY m.mezuniyet_yili 
        ORDER BY m.mezuniyet_yili;
        """
        df = get_data(sql)
        if not df.empty:
            df['mezuniyet_yili'] = df['mezuniyet_yili'].astype(str)
            st.line_chart(data=df, x="mezuniyet_yili", y="employment_rate_percentage", color="#a91b1b")

    elif secim == "🎓 6. Mezun Verileri":
        st.subheader("🎓 6. Mezun Verileri")
        st.write("Tüm mezunları ve temel bilgilerini bu ekranda görüntüleyebilirsiniz.")
        alumni_sql = """
            SELECT m.mezun_id AS "Mezun ID",
                   m.ad AS "Ad",
                   m.soyad AS "Soyad",
                   m.iletisim_bilgisi AS "İletişim",
                   m.mezuniyet_yili AS "Mezuniyet Yılı",
                   m.not_ortalamasi AS "Not Ortalaması",
                   b.bolum_adi AS "Bölüm"
            FROM Mezun m
            LEFT JOIN Bolum b ON m.bolum_id = b.bolum_id
            ORDER BY m.mezun_id;
        """
        alumni_df = get_data(alumni_sql)
        if alumni_df.empty:
            st.warning("Veritabanında görüntülenecek mezun verisi bulunamadı.")
        else:
            st.success(f"Toplam {len(alumni_df)} mezun kaydı bulundu.")
            st.dataframe(alumni_df, use_container_width=True)

