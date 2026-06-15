import streamlit as st
import requests
import urllib.parse
import qrcode
import pandas as pd
import os
from io import BytesIO
from datetime import datetime

# =========================
# GOBENG V11 PRO
# =========================

NAMA_BENGKEL = "Jasund Motor"
ALAMAT_BENGKEL = "Kp Caringin RT/RW 005/005, Sukasari, Karangtengah, Cianjur - Jawa Barat"
JAM_OPERASIONAL = "07.00 - 20.00 WIB"

NO_WA_BENGKEL = "628562287257"
NO_TELP_BENGKEL = "08562287257"

GOOGLE_MAPS_LINK = "https://maps.app.goo.gl/HG12k3keMSdLcsDw8"
LINK_GOBENG = "https://gobeng.streamlit.app"

BANNER_FILE = "banner_gobeng.png.png"
ORDER_FILE = "orders_gobeng.csv"

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


def kirim_foto_telegram(foto, caption):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    files = {"photo": foto}
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "caption": caption,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=data, files=files, timeout=15)
    except Exception:
        pass


def buat_link_wa(nama, lokasi, keluhan):
    pesan = f"""Halo {NAMA_BENGKEL}, saya butuh bantuan dari GOBENG.

Nama: {nama}
Lokasi/Patokan: {lokasi}
Keluhan: {keluhan}

Mohon segera dibantu."""
    return f"https://wa.me/{NO_WA_BENGKEL}?text={urllib.parse.quote(pesan)}"


def simpan_order(nama, lokasi, keluhan, rating="-"):
    waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    data_baru = pd.DataFrame([{
        "waktu": waktu,
        "nama": nama,
        "lokasi": lokasi,
        "keluhan": keluhan,
        "status": "Menunggu",
        "rating": rating
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
    return pd.DataFrame(columns=["waktu", "nama", "lokasi", "keluhan", "status", "rating"])


def buat_qr(link):
    qr = qrcode.QRCode(version=2, box_size=10, border=4)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


st.set_page_config(
    page_title="GOBENG V11 Pro",
    page_icon="🔧",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #000000, #151515);
    color: white;
}
label, .stTextInput label, .stTextArea label, .stSelectbox label, .stSlider label {
    color: white !important;
    font-size: 17px !important;
    font-weight: 800 !important;
}
input, textarea, select {
    color: black !important;
    background-color: white !important;
}
.hero {
    background: linear-gradient(135deg, #3b0000, #111111);
    padding: 22px;
    border-radius: 22px;
    border: 3px solid #ffcc00;
    text-align: center;
    margin-bottom: 22px;
}
.hero-title {
    color: #ff3333;
    font-size: 36px;
    font-weight: 900;
}
.hero-sub {
    color: white;
    font-size: 24px;
    font-weight: 800;
}
.card {
    background-color: #101010;
    padding: 20px;
    border-radius: 18px;
    border: 2px solid #ffcc00;
    margin-bottom: 18px;
}
.info-card {
    background-color: #222222;
    padding: 16px;
    border-radius: 14px;
    margin-bottom: 12px;
    border: 1px solid #444;
}
div.stButton > button {
    width: 100%;
    background-color: #ff3333;
    color: white;
    font-size: 22px;
    font-weight: 900;
    border-radius: 14px;
    border: none;
    padding: 16px;
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

# =========================
# HEADER
# =========================

if os.path.exists(BANNER_FILE):
    st.image(BANNER_FILE, use_container_width=True)
else:
    st.markdown("# 🔧 GOBENG")
    st.markdown("### Motor Mogok? GOBENG-IN AJA!")

st.markdown("""
<div class="hero">
    <div class="hero-title">🚨 MOTOR MOGOK?</div>
    <div class="hero-sub">Tidak perlu dorong motor lagi!</div>
    <p>Isi form atau langsung hubungi Jasund Motor.</p>
</div>
""", unsafe_allow_html=True)

# =========================
# TOMBOL CEPAT
# =========================

st.link_button(
    "💬 WHATSAPP JASUND MOTOR",
    f"https://wa.me/{NO_WA_BENGKEL}?text={urllib.parse.quote('Halo GOBENG, saya butuh bantuan bengkel.')}",
    use_container_width=True
)

st.link_button(
    "📞 TELEPON BENGKEL",
    f"tel:{NO_TELP_BENGKEL}",
    use_container_width=True
)

st.link_button(
    "🗺️ BUKA LOKASI GOOGLE MAPS",
    GOOGLE_MAPS_LINK,
    use_container_width=True
)

st.divider()

# =========================
# FORM ORDER
# =========================

st.markdown("## 🚨 Form Bantuan GOBENG")

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

catatan = st.text_area(
    "Catatan tambahan",
    placeholder="Contoh: dekat minimarket, depan masjid, pinggir jalan..."
)

foto_kendaraan = st.file_uploader(
    "Upload foto kendaraan / lokasi jika ada",
    type=["jpg", "jpeg", "png"]
)

if st.button("🚨 MINTA BANTUAN SEKARANG"):
    if nama.strip() == "" or lokasi.strip() == "":
        st.warning("Nama dan lokasi/patokan wajib diisi.")
    else:
        keluhan_lengkap = keluhan
        if catatan.strip():
            keluhan_lengkap += f" - {catatan}"

        waktu = simpan_order(nama, lokasi, keluhan_lengkap)

        pesan_telegram = f"""
🚨 <b>ORDER BARU GOBENG V11</b>

👤 Nama: {nama}
📍 Lokasi/Patokan: {lokasi}
🛠 Keluhan: {keluhan_lengkap}
⏰ Waktu: {waktu}

Segera cek pelanggan.
"""
        kirim_telegram(pesan_telegram)

        if foto_kendaraan is not None:
            caption = f"""
📸 <b>FOTO ORDER GOBENG</b>

👤 Nama: {nama}
📍 Lokasi: {lokasi}
🛠 Keluhan: {keluhan_lengkap}
"""
            kirim_foto_telegram(foto_kendaraan, caption)

        st.success("Order berhasil masuk ke GOBENG.")
        st.link_button(
            "💬 LANJUT CHAT WHATSAPP BENGKEL",
            buat_link_wa(nama, lokasi, keluhan_lengkap),
            use_container_width=True
        )

st.divider()

# =========================
# RATING PELANGGAN
# =========================

st.markdown("## ⭐ Rating Pelayanan")

rating_nama = st.text_input("Nama untuk rating")
rating = st.slider("Beri rating pelayanan Jasund Motor", 1, 5, 5)

if st.button("⭐ KIRIM RATING"):
    if rating_nama.strip() == "":
        st.warning("Nama wajib diisi.")
    else:
        waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        pesan_rating = f"""
⭐ <b>RATING BARU GOBENG</b>

👤 Nama: {rating_nama}
⭐ Rating: {rating}/5
⏰ Waktu: {waktu}
"""
        kirim_telegram(pesan_rating)
        st.success("Terima kasih, rating berhasil dikirim.")

st.divider()

# =========================
# INFO BENGKEL
# =========================

st.markdown("## 📍 Info Bengkel")

st.markdown(f"""
<div class="card">
    <h3>{NAMA_BENGKEL}</h3>
    <p>📍 {ALAMAT_BENGKEL}</p>
    <p>⏰ Jam Operasional: {JAM_OPERASIONAL}</p>
</div>
""", unsafe_allow_html=True)

st.markdown("## 🛠 Layanan")

st.markdown("""
<div class="info-card">✅ Bantuan motor mogok</div>
<div class="info-card">✅ Ban kempes / bocor</div>
<div class="info-card">✅ Servis ringan</div>
<div class="info-card">✅ Cek aki</div>
<div class="info-card">✅ Mesin bermasalah</div>
<div class="info-card">✅ Lokasi bengkel di Google Maps</div>
""", unsafe_allow_html=True)

# =========================
# ADMIN
# =========================

st.divider()

with st.expander("🔐 Admin GOBENG"):
    password = st.text_input("Password Admin", type="password")

    if password == "admin123":
        tab1, tab2, tab3 = st.tabs(["📋 Order Masuk", "📊 Statistik", "📱 QR Code"])

        with tab1:
            st.markdown("### 📋 Order Masuk")
            data = baca_order()

            if data.empty:
                st.info("Belum ada order.")
            else:
                st.dataframe(data.sort_values(by="waktu", ascending=False), use_container_width=True)

                csv = data.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "⬇️ Download Order CSV",
                    data=csv,
                    file_name="order_gobeng.csv",
                    mime="text/csv"
                )

        with tab2:
            st.markdown("### 📊 Statistik")
            data = baca_order()
            total = len(data)
            menunggu = len(data[data["status"] == "Menunggu"]) if not data.empty else 0

            col1, col2 = st.columns(2)
            col1.metric("Total Order", total)
            col2.metric("Menunggu", menunggu)

        with tab3:
            st.markdown("### 📱 QR Code GOBENG")
            qr_img = buat_qr(LINK_GOBENG)
            st.image(qr_img, width=300)

            st.download_button(
                "⬇️ Download QR Code",
                data=qr_img,
                file_name="qr_gobeng_v11.png",
                mime="image/png"
            )

    elif password:
        st.error("Password salah.")

st.caption("GOBENG V11 Pro | Jasund Motor | Solusi Cepat Saat Kendaraan Bermasalah")
