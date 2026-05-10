import streamlit as st
import pandas as pd
import pyodbc
import plotly.express as px

# ==========================================
# SAYFA AYARLARI VE ÖZEL TASARIM (CSS)
# ==========================================
st.set_page_config(page_title="ATÜ Mezun Bilgi Sistemi", page_icon="🎓", layout="wide")

# ATÜ Kimliğine (Bordo/Kırmızı) uygun özel CSS
custom_css = """
<style>
    /* Ortak Kutu (Card) Tasarımı */
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
# VERİTABANI BAĞLANTI AYARLARI
# ==========================================
@st.cache_resource
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

@st.cache_data
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
            except ValueError:
                pass
    return df

# ==========================================
# ARAYÜZ (SIDEBAR - YAN MENÜ)
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2936/2936769.png", width=100)
st.sidebar.title("ATÜ Menü")

menu = [
    "🏠 Ana Sayfa",
    "📊 1. Bölüm Bazlı Mezun Sayısı",
    "🏢 2. Sektör Bazlı İstihdam",
    "💰 3. Bölüm Bazlı Ortalama Maaş",
    "🔄 4. İş Değiştirme Oranı",
    "📈 5. Yıllara Göre İstihdam"
]

secim = st.sidebar.radio("Sayfalar", menu)

st.sidebar.markdown("---")
st.sidebar.info("📌 **Proje:** Mezun ve Kariyer Takip Sistemi\n\nBu sistem 3NF normalizasyon kurallarına göre tasarlanmıştır.")

# ==========================================
# ANA SAYFA TASARIMI
# ==========================================
if secim == "🏠 Ana Sayfa":
    
    # 1. Kısım: Üst Banner
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
            <div style="text-align: center;">
                <span style="font-size: 24px;">🌐</span><br>
                <span style="font-size: 12px; color: #f8fafc;">English</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.write("") 

    # 2. Kısım: Metrik Kartları
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; height: 140px;">
                <div class="card-title">🚪 Mezunlar Portalına</div><br>
                <a href="#" class="login-btn">Giriş Yap</a>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; height: 140px;">
                <div class="card-title">⚙️ Önlisans Mezun Sayısı</div>
                <div class="num-green">58.756</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; height: 140px;">
                <div class="card-title">🎓 Lisans Mezun Sayısı</div>
                <div class="num-blue">76.762</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; height: 140px;">
                <div class="card-title">🏅 Lisansüstü Mezun Sayısı</div>
                <div class="num-purple">12.734</div>
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # 3. Kısım: Duyurular ve Etkinlikler
    b_col1, b_col2, b_col3 = st.columns(3)
    with b_col1:
        st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; min-height: 250px;">
                <h3 style="margin-top:0; border-bottom: 2px solid #a91b1b; padding-bottom: 5px;">📢 ATÜ Duyurular</h3>
                <div class="list-item"><span>ATÜ Kariyer Günleri Etkinliği</span><span class="list-date">10.05.2026</span></div>
                <div class="list-item"><span>Mezuniyet Töreni Bilgilendirmesi</span><span class="list-date">15.06.2026</span></div>
                <div class="list-item"><span>TÜBİTAK Proje Başvuruları Başladı</span><span class="list-date">20.04.2026</span></div>
                <div class="list-item"><span>Erasmus+ Değişim Programı İlanı</span><span class="list-date">01.03.2026</span></div>
            </div>
        """, unsafe_allow_html=True)
    with b_col2:
        st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; min-height: 250px;">
                <h3 style="margin-top:0; border-bottom: 2px solid #a91b1b; padding-bottom: 5px;">📰 Haberler</h3>
                <div class="empty-state">Şu an için güncel haber bulunmamaktadır.</div>
            </div>
        """, unsafe_allow_html=True)
    with b_col3:
        st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; min-height: 250px;">
                <h3 style="margin-top:0; border-bottom: 2px solid #a91b1b; padding-bottom: 5px;">📅 Etkinlikler</h3>
                <div class="empty-state">Planlanan etkinlik bulunmamaktadır.</div>
            </div>
        """, unsafe_allow_html=True)

    # 4. Kısım: Dünya Haritası (Geliştirme Önizlemesi Notuyla)
    st.write("---")
    st.markdown("<h3 style='text-align: center; color: #1e293b;'>🌍 Dünyada Mezunlarımız (Geliştirme Önizlemesi)</h3>", unsafe_allow_html=True)
    
    st.caption("ℹ️ *Not: Bu interaktif harita, ileriki aşamalarda veritabanına 'Çalışılan Ülke' niteliği eklendiğinde sistemin yeteneklerini göstermek amacıyla örnek (dummy) veriyle tasarlanmıştır.*")
    
    map_data = pd.DataFrame({
        'Country': ['Turkey', 'United States', 'Germany', 'United Kingdom', 'France', 'Canada', 'Australia', 'Netherlands', 'Italy', 'Spain', 'Russian Federation', 'Brazil'],
        'Mezun Sayısı': [58756, 1250, 850, 450, 300, 250, 200, 400, 150, 100, 50, 20]
    })
    
    fig = px.choropleth(map_data, 
                        locations="Country", 
                        locationmode="country names",
                        color="Mezun Sayısı", 
                        color_continuous_scale="Reds", 
                        hover_name="Country")
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0), 
        geo=dict(showframe=False, showcoastlines=True, projection_type='equirectangular')
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# SQL RAPOR SAYFALARI
# ==========================================
elif secim == "📊 1. Bölüm Bazlı Mezun Sayısı":
    st.subheader("📊 Bölüm Bazlı Toplam Mezun Sayısı")
    sql = "SELECT d.department_name, COUNT(a.alumni_id) AS total_alumni_count FROM Department d LEFT JOIN Alumni a ON d.department_id = a.department_id GROUP BY d.department_name;"
    df = get_data(sql)
    col1, col2 = st.columns(2)
    with col1: st.dataframe(df, use_container_width=True)
    with col2: st.bar_chart(data=df, x="department_name", y="total_alumni_count", color="#a91b1b")

elif secim == "🏢 2. Sektör Bazlı İstihdam":
    st.subheader("🏢 Sektör Bazlı İstihdam Dağılımı")
    sql = "SELECT c.sector, COUNT(ch.career_id) AS employee_count FROM Career_History ch INNER JOIN Company c ON ch.company_id = c.company_id GROUP BY c.sector;"
    df = get_data(sql)
    col1, col2 = st.columns(2)
    with col1: st.dataframe(df, use_container_width=True)
    with col2: st.bar_chart(data=df, x="sector", y="employee_count", color="#a91b1b")

elif secim == "💰 3. Bölüm Bazlı Ortalama Maaş":
    st.subheader("💰 Bölümlere Göre Ortalama Maaş Analizi")
    sql = "SELECT d.department_name, AVG(ch.salary) AS average_salary FROM Department d INNER JOIN Alumni a ON d.department_id = a.department_id INNER JOIN Career_History ch ON a.alumni_id = ch.alumni_id GROUP BY d.department_name;"
    df = get_data(sql)
    col1, col2 = st.columns(2)
    with col1: st.dataframe(df, use_container_width=True)
    with col2: st.bar_chart(data=df, x="department_name", y="average_salary", color="#a91b1b")

elif secim == "🔄 4. İş Değiştirme Oranı":
    st.subheader("🔄 Ortalama İş Değiştirme Oranı")
    sql = "SELECT (COUNT(ch.career_id) * 1.0) / COUNT(DISTINCT ch.alumni_id) AS average_job_turnover_rate FROM Career_History ch;"
    df = get_data(sql)
    oran = df['average_job_turnover_rate'].iloc[0] if not df.empty else 0
    st.metric(label="Mezun Başına Düşen Ortalama İş Sayısı", value=f"{oran:.2f}", delta="Sektör ortalamasının üstünde", delta_color="normal")
    st.dataframe(df, use_container_width=True)

elif secim == "📈 5. Yıllara Göre İstihdam":
    st.subheader("📈 Mezuniyet Yılına Göre İstihdam Oranı (%)")
    sql = """
    SELECT a.graduation_year, 
    COUNT(DISTINCT a.alumni_id) AS total_alumni,
    COUNT(DISTINCT CASE WHEN ch.end_date IS NULL THEN ch.alumni_id END) AS active_employees,
    ((COUNT(DISTINCT CASE WHEN ch.end_date IS NULL THEN ch.alumni_id END) * 1.0) / 
    NULLIF(COUNT(DISTINCT a.alumni_id), 0)) * 100 AS employment_rate_percentage
    FROM Alumni a LEFT JOIN Career_History ch ON a.alumni_id = ch.alumni_id
    GROUP BY a.graduation_year 
    ORDER BY a.graduation_year;
    """
    df = get_data(sql)
    if not df.empty:
        df['graduation_year'] = df['graduation_year'].astype(str)
        st.dataframe(df, use_container_width=True)
        st.line_chart(data=df, x="graduation_year", y="employment_rate_percentage", color="#a91b1b")
