import streamlit as st
import requests
import urllib.parse
import qrcode
from io import BytesIO
from datetime import datetime

# =========================
# GOBENG V8.1 PRO
# =========================

NAMA_APP = "GOBENG"
SLOGAN = "Motor Mogok? GOBENG-IN AJA!"

NAMA_BENGKEL = "Jasund Motor"
ALAMAT_BENGKEL = "Kp Caringin RT/RW 005/005, Sukasari, Kec. Karangtengah, Kabupaten Cianjur, Jawa Barat 43281"
JAM_OPERASIONAL = "07.00 - 20.00 WIB"

NO_WA_BENGKEL = "628562287257"
GOOGLE_MAPS_LINK = "https://maps.app.goo.gl/f5HMLq8Ro1rcdDcn8"

# Ganti dengan link website GOBENG yang sudah online
LINK_GOBENG = "https://gobeng.streamlit.app"

# Telegram
TELEGRAM_BOT_TOKEN = "8742663611:AAE4hrUYrM8gagxr9qQCPd2N71TH9czF3tY"
TELEGRAM_CHAT_ID = "8951538688"


def kirim_telegram(pesan):

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

    


def buat_link_wa(nama, lokasi, keluhan):
    pesan = f"""Halo {NAMA_BENGKEL}, saya butuh bantuan dari GOBENG.

Nama: {nama}
Lokasi: {lokasi}
Keluhan: {keluhan}

Mohon segera dibantu."""
    return f"https://wa.me/{NO_WA_BENGKEL}?text={urllib.parse.quote(pesan)}"


def buat_qr(link):
    qr = qrcode.QRCode(
        version=2,
        box_size=10,
        border=4
    )
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


st.set_page_config(
    page_title="GOBENG V8.1 Pro",
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

.logo {
    font-size: 56px;
    font-weight: 900;
    color: #ffcc00;
    text-align: center;
    margin-bottom: 0px;
}

.slogan {
    font-size: 25px;
    font-weight: 800;
    color: white;
    text-align: center;
    margin-bottom: 25px;
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
    font-size: 24px;
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
    font-size: 22px;
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
st.image("banner_gobeng.png.png", use_container_width=True)
st.markdown('<div class="logo">🔧 GOBENG</div>', unsafe_allow_html=True)
st.markdown(f'<div class="slogan">{SLOGAN}</div>', unsafe_allow_html=True)

menu = st.sidebar.radio(
    "Menu GOBENG",
    [
        "🚨 Bantuan Mogok",
        "📍 Info Bengkel",
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
    lokasi = st.text_input("Lokasi motor mogok")

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

    catatan = st.text_area(
        "Catatan tambahan",
        placeholder="Contoh: motor mati di pinggir jalan dekat minimarket..."
    )

    if st.button("🚨 MINTA BANTUAN SEKARANG"):
        if nama.strip() == "" or lokasi.strip() == "":
            st.warning("Nama dan lokasi wajib diisi.")
        else:
            keluhan_lengkap = keluhan
            if catatan.strip():
                keluhan_lengkap += f" - {catatan}"

            waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            pesan_telegram = f"""
🚨 <b>ORDER BARU GOBENG V8.1 PRO</b>

👤 Nama: {nama}
📍 Lokasi: {lokasi}
🛠 Keluhan: {keluhan_lengkap}
⏰ Waktu: {waktu}

Segera cek pelanggan.
"""
            kirim_telegram(pesan_telegram)

            st.success("Data berhasil masuk ke GOBENG.")
            st.link_button(
                "💬 LANJUT CHAT WHATSAPP BENGKEL",
                buat_link_wa(nama, lokasi, keluhan_lengkap),
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
    st.link_button(
        "💬 WHATSAPP BENGKEL",
        f"https://wa.me/{NO_WA_BENGKEL}?text={pesan_cepat}",
        use_container_width=True
    )

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

    link_input = st.text_input(
        "Link GOBENG untuk QR",
        value=LINK_GOBENG
    )

    qr_img = buat_qr(link_input)

    st.image(qr_img, caption="QR Code GOBENG", width=330)

    st.download_button(
        label="⬇️ DOWNLOAD QR CODE PNG",
        data=qr_img,
        file_name="qr_gobeng_v8_1_pro.png",
        mime="image/png"
    )

    st.success("QR ini bisa dipasang di banner: MOTOR MOGOK? GOBENG-IN AJA!")

st.divider()
st.caption("GOBENG V8.1 Pro | Solusi Cepat Saat Kendaraan Bermasalah")
