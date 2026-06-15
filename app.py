import streamlit as st
import requests
import urllib.parse
import qrcode
import pandas as pd
import os
from io import BytesIO
from datetime import datetime

try:
    from streamlit_js_eval import get_geolocation
except Exception:
    get_geolocation = None


# =========================
# GOBENG V9 PRO
# =========================

NAMA_APP = "GOBENG"
SLOGAN = "Motor Mogok? GOBENG-IN AJA!"

NAMA_BENGKEL = "Jasund Motor"
ALAMAT_BENGKEL = "Kp Caringin RT/RW 005/005, Sukasari, Karangtengah, Cianjur - Jawa Barat"
JAM_OPERASIONAL = "07.00 - 20.00 WIB"

NO_WA_BENGKEL = "628562287257"
NO_TELP_BENGKEL = "08562287257"

GOOGLE_MAPS_LINK = "https://maps.app.goo.gl/28eMg2nb51No7Pdk6"
LINK_GOBENG = "https://gobeng.streamlit.app"

BANNER_FILE = "banner_gobeng.png.png"
ORDER_FILE = "orders_gobeng.csv"

# Telegram
TELEGRAM_BOT_TOKEN = "8742663611:AAE4hrUYrM8gagxr9qQCPd2N71TH9czF3tY"
TELEGRAM_CHAT_ID = "8951538688"


# =========================
# FUNGSI DASAR
# =========================

def kirim_telegram(pesan):
    if TELEGRAM_BOT_TOKEN == "ISI_TOKEN_TELEGRAM_KAMU":
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": pesan,
        "parse_mode": "HTML"
    }

    try:
        requests.post(url, data=data, timeout=10)
    except Exception:
        pass


def buat_link_wa(nama, lokasi, keluhan, link_lokasi):
    pesan = f"""Halo {NAMA_BENGKEL}, saya butuh bantuan dari GOBENG.

Nama: {nama}
Lokasi tertulis: {lokasi}
Keluhan: {keluhan}
Lokasi GPS/Maps: {link_lokasi}

Mohon segera dibantu."""
    return f"https://wa.me/{NO_WA_BENGKEL}?text={urllib.parse.quote(pesan)}"


def buat_qr(link):
    qr = qrcode.QRCode(version=2, box_size=10, border=4)
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


def simpan_order(nama, lokasi, keluhan, link_lokasi):
    waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    data_baru = pd.DataFrame([{
        "waktu": waktu,
        "nama": nama,
        "lokasi": lokasi,
        "keluhan": keluhan,
        "link_lokasi": link_lokasi,
        "status": "Menunggu"
    }])

    if os.path.exists(ORDER_FILE):
        data_lama = pd.read_csv(ORDER_FILE)
        data = pd.concat([data_lama, data_baru], ignore_index=True)
    else:
        data = data_baru

    data.to_csv(ORDER_FILE, index=False)
    return waktu


def baca_order():
    if os.path.exists(ORDER_FILE):
        return pd.read_csv(ORDER_FILE)
    return pd.DataFrame(columns=["waktu", "nama", "lokasi", "keluhan", "link_lokasi", "status"])


# =========================
# TAMPILAN
# =========================

st.set_page_config(
    page_title="GOBENG V9 Pro",
    page_icon="🔧",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #000000, #151515);
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #f2f2f2;
}

label, .stTextInput label, .stTextArea label, .stSelectbox label {
    color: white !important;
    font-size: 17px !important;
    font-weight: 800 !important;
}

input, textarea, select {
    color: black !important;
    background-color: white !important;
}

.hero {
    background: linear-gradient(135deg, #330000, #111111);
    padding: 25px;
    border-radius: 22px;
    border: 3px solid #ffcc00;
    text-align: center;
    margin-bottom: 25px;
}

.hero-title {
    color: #ff3333;
    font-size: 34px;
    font-weight: 900;
}

.hero-sub {
    color: white;
    font-size: 23px;
    font-weight: 800;
}

.card {
    background-color: #101010;
    padding: 22px;
    border-radius: 18px;
    border: 2px solid #ffcc00;
    margin-bottom: 20px;
}

.service-box {
    background-color: #222;
    padding: 15px;
    border-radius: 14px;
    border: 1px solid #444;
    margin-bottom: 10px;
}

div.stButton > button {
    width: 100%;
    background-color: #ff3333;
    color: white;
    font-size: 21px;
    font-weight: 900;
    border-radius: 14px;
    border: none;
    padding: 15px;
}

div.stDownloadButton > button {
    width: 100%;
    background-color: #ffcc00;
    color: black;
    font-size: 18px;
    font-weight: 900;
    border-radius: 12px;
    border: none;
    padding: 12px;
}
</style>
""", unsafe_allow_html=True)


# Banner dashboard
if os.path.exists(BANNER_FILE):
    st.image(BANNER_FILE, use_container_width=True)
else:
    st.markdown("## 🔧 GOBENG")
    st.markdown(f"### {SLOGAN}")

st.success("📍 Isi form di bawah. Jika GPS aktif, lokasi pelanggan bisa terkirim langsung ke WhatsApp dan Telegram.")

menu = st.sidebar.radio(
    "Menu GOBENG",
    [
        "🚨 Bantuan Mogok",
        "📍 Info Bengkel",
        "📋 Order Masuk",
        "📊 Statistik",
        "📱 QR Code Banner"
    ]
)


# =========================
# BANTUAN MOGOK
# =========================

if menu == "🚨 Bantuan Mogok":
    st.markdown("""
    <div class="hero">
        <div class="hero-title">🚨 MOTOR MOGOK?</div>
        <div class="hero-sub">Tidak perlu dorong motor lagi!</div>
        <p>Isi data di bawah ini, lalu lanjut WhatsApp bengkel.</p>
    </div>
    """, unsafe_allow_html=True)

    nama = st.text_input("Nama pelanggan")
    lokasi = st.text_input("Lokasi motor mogok / patokan")
    keluhan = st.selectbox(
        "Keluhan kendaraan",
        [
            "Motor mogok",
            "Ban kempes / bocor",
            "Aki tekor / soak",
            "Mesin susah hidup",
            "Butuh servis ringan",
            "Lainnya"
        ]
    )
    catatan = st.text_area("Catatan tambahan", placeholder="Contoh: dekat minimarket, depan masjid, pinggir jalan...")

   st.markdown("### 📍 Lokasi GPS Otomatis")

if "link_lokasi" not in st.session_state:
    st.session_state.link_lokasi = "Tidak menggunakan GPS"

if st.button("📍 AMBIL LOKASI SAYA"):
    if get_geolocation is not None:
        lokasi_gps = get_geolocation()

        if lokasi_gps and "coords" in lokasi_gps:
            lat = lokasi_gps["coords"]["latitude"]
            lon = lokasi_gps["coords"]["longitude"]

            st.session_state.link_lokasi = f"https://maps.google.com/?q={lat},{lon}"
            st.success("✅ Lokasi GPS berhasil diambil.")
            st.write(st.session_state.link_lokasi)
        else:
            st.warning("GPS belum terbaca. Jika muncul izin lokasi, klik Izinkan lalu tekan tombol ini lagi.")
    else:
        st.warning("Fitur GPS belum aktif. Cek requirements.txt.")

link_lokasi = st.session_state.link_lokasi

if link_lokasi != "Tidak menggunakan GPS":
    st.success("📍 Lokasi GPS siap dikirim ke WhatsApp dan Telegram.")
else:
    st.info("GPS belum diambil. Jika tidak sempat, order tetap bisa dikirim memakai patokan lokasi.")
    if st.button("🚨 MINTA BANTUAN SEKARANG"):
        if nama.strip() == "" or lokasi.strip() == "":
            st.warning("Nama dan lokasi/patokan wajib diisi.")
        else:
            keluhan_lengkap = keluhan
            if catatan.strip():
                keluhan_lengkap += f" - {catatan}"

            waktu = simpan_order(nama, lokasi, keluhan_lengkap, link_lokasi)

            pesan_telegram = f"""
🚨 <b>ORDER BARU GOBENG V9 PRO</b>

👤 Nama: {nama}
📍 Lokasi/Patokan: {lokasi}
🛠 Keluhan: {keluhan_lengkap}
🗺 GPS/Maps: {link_lokasi}
⏰ Waktu: {waktu}

Segera cek pelanggan.
"""
            kirim_telegram(pesan_telegram)

            st.success("Order berhasil masuk ke GOBENG.")
            st.link_button(
                "💬 LANJUT CHAT WHATSAPP BENGKEL",
                buat_link_wa(nama, lokasi, keluhan_lengkap, link_lokasi),
                use_container_width=True
            )

    st.markdown("### 🛠 Bantuan yang tersedia")
    st.markdown("""
    <div class="service-box">✅ Motor mogok</div>
    <div class="service-box">✅ Ban kempes / bocor</div>
    <div class="service-box">✅ Aki tekor / soak</div>
    <div class="service-box">✅ Mesin bermasalah</div>
    """, unsafe_allow_html=True)


# =========================
# INFO BENGKEL
# =========================

elif menu == "📍 Info Bengkel":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 📍 Informasi Bengkel")
    st.write(f"**{NAMA_BENGKEL}**")
    st.write(f"📍 {ALAMAT_BENGKEL}")
    st.write(f"⏰ Jam Operasional: {JAM_OPERASIONAL}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.link_button("📍 BUKA GOOGLE MAPS", GOOGLE_MAPS_LINK, use_container_width=True)

    pesan_cepat = urllib.parse.quote("Halo GOBENG, saya ingin tanya layanan bengkel.")
    st.link_button("💬 WHATSAPP BENGKEL", f"https://wa.me/{NO_WA_BENGKEL}?text={pesan_cepat}", use_container_width=True)

    st.link_button("📞 TELEPON BENGKEL", f"tel:{NO_TELP_BENGKEL}", use_container_width=True)

    st.markdown("## 🛠 Layanan GOBENG")
    st.write("""
✅ Bantuan motor mogok  
✅ Ban kempes / bocor  
✅ Servis ringan  
✅ Cek aki  
✅ Mesin bermasalah  
✅ Lihat lokasi bengkel  
✅ Hubungi mekanik lebih cepat  
""")


# =========================
# ORDER MASUK
# =========================

elif menu == "📋 Order Masuk":
    st.markdown("## 📋 Order Masuk GOBENG")

    data = baca_order()

    if data.empty:
        st.info("Belum ada order masuk.")
    else:
        data_tampil = data.sort_values(by="waktu", ascending=False)
        st.dataframe(data_tampil, use_container_width=True)

        csv = data_tampil.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Data Order CSV",
            data=csv,
            file_name="order_gobeng.csv",
            mime="text/csv"
        )


# =========================
# STATISTIK
# =========================

elif menu == "📊 Statistik":
    st.markdown("## 📊 Statistik GOBENG")

    data = baca_order()

    total_order = len(data)
    menunggu = len(data[data["status"] == "Menunggu"]) if not data.empty else 0

    col1, col2 = st.columns(2)
    col1.metric("Total Order", total_order)
    col2.metric("Order Menunggu", menunggu)

    st.info("Statistik ini membantu melihat apakah QR banner mulai menghasilkan pelanggan.")


# =========================
# QR CODE
# =========================

elif menu == "📱 QR Code Banner":
    st.markdown("""
    <div class="hero">
        <div class="hero-title">📱 QR CODE GOBENG</div>
        <div class="hero-sub">Untuk banner dan stiker</div>
        <p>Saat discan, pelanggan masuk dulu ke aplikasi GOBENG.</p>
    </div>
    """, unsafe_allow_html=True)

    link_input = st.text_input("Link GOBENG untuk QR", value=LINK_GOBENG)

    qr_img = buat_qr(link_input)

    st.image(qr_img, caption="QR Code GOBENG", width=330)

    st.download_button(
        label="⬇️ DOWNLOAD QR CODE PNG",
        data=qr_img,
        file_name="qr_gobeng_v9_pro.png",
        mime="image/png"
    )

    st.success("QR ini bisa dipasang di banner: MOTOR MOGOK? GOBENG-IN AJA!")


st.divider()
st.caption("GOBENG V9 Pro | Jasund Motor | Solusi Cepat Saat Kendaraan Bermasalah")
