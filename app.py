import streamlit as st
import urllib.parse
from datetime import datetime

st.set_page_config(page_title="GOBENG", page_icon="🏍️", layout="centered")

NOMOR_WA = "628562287257"

st.markdown("""
<style>
.stApp { background: #f7f8fa; }
.block-container { max-width: 720px; padding-top: 25px; }

.hero {
    background: linear-gradient(135deg, #e60000, #ff4b4b);
    padding: 28px;
    border-radius: 22px;
    color: white;
    text-align: center;
    box-shadow: 0 8px 25px rgba(230,0,0,0.25);
}
.hero h1 { font-size: 42px; margin: 0; }
.hero p { font-size: 17px; margin-top: 8px; }

.card {
    background: white;
    padding: 18px;
    border-radius: 18px;
    margin-top: 16px;
    box-shadow: 0 5px 18px rgba(0,0,0,0.06);
    border: 1px solid #eeeeee;
}
.stat {
    background: white;
    padding: 14px;
    border-radius: 14px;
    text-align: center;
    box-shadow: 0 3px 12px rgba(0,0,0,0.05);
}
.service {
    background: #fff4f4;
    padding: 12px;
    border-radius: 14px;
    margin: 6px 0;
    border: 1px solid #ffd0d0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🏍️ GOBENG</h1>
    <p>Bengkel Panggilan Online • Cepat • Praktis • Terpercaya</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
<b>Motor mogok? Ban bocor?</b><br>
GOBENG siap membantu Anda dengan teknisi panggilan langsung ke lokasi.
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="stat">⭐<br><b>4.9</b><br>Rating</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="stat">🔧<br><b>24 Jam</b><br>Siaga</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="stat">📍<br><b>Cianjur</b><br>Area</div>', unsafe_allow_html=True)

st.markdown("### 🔧 Layanan Tersedia")
st.markdown("""
<div class="service">🛞 Tambal Ban</div>
<div class="service">🛵 Motor Mogok</div>
<div class="service">🛢️ Ganti Oli</div>
<div class="service">🔋 Aki Soak</div>
<div class="service">⚙️ Servis Ringan</div>
""", unsafe_allow_html=True)

st.markdown("### 📝 Form Pemesanan")

nama = st.text_input("Nama Pelanggan")
hp = st.text_input("Nomor HP / WhatsApp")
kendaraan = st.selectbox("Jenis Kendaraan", ["Motor", "Mobil"])

layanan = st.selectbox(
    "Pilih Layanan",
    ["Tambal Ban", "Motor Mogok", "Ganti Oli", "Servis Ringan", "Isi Angin", "Ganti Busi", "Aki Soak"]
)

alamat = st.text_area("Alamat Lengkap")
patokan = st.text_input("Patokan Lokasi")
keluhan = st.text_area("Keluhan Kendaraan")

foto = st.file_uploader(
    "Upload Foto Kerusakan Kendaraan",
    type=["jpg", "jpeg", "png"]
)

if foto:
    st.image(foto, caption="Foto kerusakan berhasil diupload", use_container_width=True)

harga = {
    "Tambal Ban": "Mulai Rp15.000",
    "Motor Mogok": "Mulai Rp20.000",
    "Ganti Oli": "Jasa mulai Rp5.000",
    "Servis Ringan": "Mulai Rp20.000",
    "Isi Angin": "Mulai Rp5.000",
    "Ganti Busi": "Jasa mulai Rp10.000",
    "Aki Soak": "Menyesuaikan kondisi kendaraan",
}

st.success(f"Estimasi biaya: {harga[layanan]}")

st.warning("""
🚨 Biaya panggilan menyesuaikan jarak lokasi pelanggan.

Estimasi final akan diinformasikan teknisi sebelum pengerjaan.
""")

st.info("Setelah WhatsApp terbuka, pelanggan bisa langsung mengirim share location kepada teknisi.")

if st.button("📲 PANGGIL TEKNISI SEKARANG", use_container_width=True):
    if nama and hp and alamat and keluhan:
        order_id = "GB-" + datetime.now().strftime("%Y%m%d-%H%M%S")
        status_foto = "Sudah upload foto kerusakan" if foto else "Belum upload foto"

        pesan = f"""
Halo GOBENG

ORDER ID: {order_id}

Saya ingin panggil teknisi.

Nama: {nama}
No HP/WA: {hp}
Jenis Kendaraan: {kendaraan}
Layanan: {layanan}
Estimasi Biaya: {harga[layanan]}
Alamat: {alamat}
Patokan: {patokan}
Keluhan: {keluhan}
Foto Kerusakan: {status_foto}

Catatan:
Saya akan mengirim share location lewat WhatsApp setelah ini.

Mohon bantuan teknisi Joni datang ke lokasi.
"""
        link = f"https://wa.me/{NOMOR_WA}?text={urllib.parse.quote(pesan)}"
        st.success("Order berhasil dibuat.")
        st.markdown(f"### [➡ LANJUT KE WHATSAPP TEKNISI]({link})")
    else:
        st.warning("Mohon isi nama, nomor HP, alamat, dan keluhan dulu.")

st.markdown("---")
st.caption("© GOBENG - Bengkel Panggilan Online")
