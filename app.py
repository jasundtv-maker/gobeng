import streamlit as st
import requests
import urllib.parse
import qrcode
from io import BytesIO
from datetime import datetime

# =========================
# GOBENG V8 PRO
# =========================

NAMA_APP = "GOBENG"
SLOGAN = "Motor Mogok? GOBENG-IN AJA!"

NAMA_BENGKEL = "Bengkel Joni"
ALAMAT_BENGKEL = "Isi alamat bengkel kamu di sini"
JAM_OPERASIONAL = "08.00 - 20.00 WIB"

NO_WA_BENGKEL = "628xxxxxxxxxx"  # ganti nomor WA
GOOGLE_MAPS_LINK = "https://maps.google.com/?q=Bengkel+Joni"

# isi dengan link website GOBENG yang online
LINK_GOBENG = "https://link-gobeng-kamu.streamlit.app"

# Telegram
TELEGRAM_BOT_TOKEN = "ISI_TOKEN_BOT_TELEGRAM"
TELEGRAM_CHAT_ID = "ISI_CHAT_ID_TELEGRAM"


def kirim_telegram(pesan):
    if TELEGRAM_BOT_TOKEN == "ISI_TOKEN_BOT_TELEGRAM":
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": pesan,
        "parse_mode": "HTML"
    }

    try:
        requests.post(url, data=data, timeout=10)
    except:
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
    page_title="GOBENG V8 Pro",
    page_icon="🔧",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #000000, #1a1a1a);
    color: white;
}
.logo {
    font-size: 52px;
    font-weight: 900;
    color: #ffcc00;
    text-align: center;
}
.slogan {
    font-size: 24px;
    font-weight: 700;
    color: white;
    text-align: center;
}
.card {
    background-color: #111111;
    padding: 20px;
    border-radius: 18px;
    border: 2px solid #ffcc00;
    margin-bottom: 20px;
}
.big-warning {
    font-size: 30px;
    font-weight: 900;
    color: #ff3333;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="logo">🔧 GOBENG</div>', unsafe_allow_html=True)
st.markdown(f'<div class="slogan">{SLOGAN}</div>', unsafe_allow_html=True)

st.divider()

menu = st.sidebar.radio(
    "Menu GOBENG",
    [
        "🚨 Bantuan Mogok",
        "📍 Info Bengkel",
        "📱 QR Code Banner"
    ]
)

# =========================
# MENU BANTUAN MOGOK
# =========================

if menu == "🚨 Bantuan Mogok":
    st.markdown('<div class="big-warning">🚨 MOTOR MOGOK?</div>', unsafe_allow_html=True)
    st.markdown("### Tidak perlu dorong motor lagi.")
    st.write("Isi data di bawah ini, lalu hubungi bengkel melalui WhatsApp.")

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

    if st.button("🚨 Minta Bantuan Sekarang"):
        if nama.strip() == "" or lokasi.strip() == "":
            st.warning("Nama dan lokasi wajib diisi.")
        else:
            keluhan_lengkap = keluhan
            if catatan.strip():
                keluhan_lengkap += f" - {catatan}"

            waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            pesan_telegram = f"""
🚨 <b>ORDER BARU GOBENG V8 PRO</b>

👤 Nama: {nama}
📍 Lokasi: {lokasi}
🛠 Keluhan: {keluhan_lengkap}
⏰ Waktu: {waktu}

Segera cek pelanggan.
"""
            kirim_telegram(pesan_telegram)

            st.success("Data berhasil masuk ke GOBENG.")
            st.link_button(
                "💬 Lanjut Chat WhatsApp Bengkel",
                buat_link_wa(nama, lokasi, keluhan_lengkap)
            )

# =========================
# MENU INFO BENGKEL
# =========================

elif menu == "📍 Info Bengkel":
    st.markdown("## 📍 Informasi Bengkel")

    st.info(f"""
**{NAMA_BENGKEL}**

📍 {ALAMAT_BENGKEL}

⏰ Jam Operasional: {JAM_OPERASIONAL}
""")

    st.link_button("📍 Buka Google Maps", GOOGLE_MAPS_LINK)

    pesan_cepat = urllib.parse.quote(
        "Halo GOBENG, saya ingin tanya layanan bengkel."
    )

    st.link_button(
        "💬 WhatsApp Bengkel",
        f"https://wa.me/{NO_WA_BENGKEL}?text={pesan_cepat}"
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
# MENU QR CODE
# =========================

elif menu == "📱 QR Code Banner":
    st.markdown("## 📱 QR Code GOBENG")
    st.write("QR ini untuk banner dan stiker. Saat discan, pelanggan masuk dulu ke aplikasi GOBENG.")

    link_input = st.text_input(
        "Link GOBENG untuk QR",
        value=LINK_GOBENG
    )

    qr_img = buat_qr(link_input)

    st.image(
        qr_img,
        caption="QR Code GOBENG",
        width=300
    )

    st.download_button(
        label="⬇️ Download QR Code PNG",
        data=qr_img,
        file_name="qr_gobeng_v8_pro.png",
        mime="image/png"
    )

    st.success("Gunakan QR ini untuk banner: MOTOR MOGOK? GOBENG-IN AJA!")

st.divider()
st.caption("GOBENG V8 Pro | Solusi Cepat Saat Kendaraan Bermasalah")
