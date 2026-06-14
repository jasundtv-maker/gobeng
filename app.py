import streamlit as st
import urllib.parse
from datetime import datetime

st.set_page_config(page_title="GOBENG", page_icon="🏍️", layout="centered")

NOMOR_WA = "628562287257"

st.markdown("""
<style>
.main {
    background-color: #0f0f0f;
}
.stApp {
    background: linear-gradient(180deg, #111111 0%, #1c1c1c 100%);
}
h1, h2, h3, p, label, span {
    color: #ffffff !important;
}
.hero {
    background: linear-gradient(135deg, #b30000, #ff3b3b);
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0px 8px 25px rgba(255,0,0,0.25);
}
.hero h1 {
    font-size: 42px;
    margin-bottom: 5px;
}
.hero p {
    font-size: 18px;
}
.card {
    background-color: #202020;
    padding: 18px;
    border-radius: 16px;
    margin-bottom: 15px;
    border: 1px solid #333333;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🏍️ GOBENG</h1>
    <p>Motor Mogok? Ban Bocor? GOBENG Aja!</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
<b>Layanan Bengkel Panggilan Online</b><br>
Tambal ban, motor mogok, ganti oli, servis ringan, isi angin, ganti busi, dan aki soak.
</div>
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
    "Motor Mogok": "Mulai Rp30.000",
    "Ganti Oli": "Mulai Rp20.000 jasa saja",
    "Servis Ringan": "Mulai Rp35.000",
    "Isi Angin": "Mulai Rp5.000",
    "Ganti Busi": "Mulai Rp15.000 jasa saja",
    "Aki Soak": "Mulai Rp30.000",
}

st.markdown(f"""
<div class="card">
<b>Estimasi Biaya:</b><br>
{harga[layanan]}
</div>
""", unsafe_allow_html=True)

st.info("Setelah WhatsApp terbuka, pelanggan bisa langsung mengirim share location kepada teknisi.")

if st.button("📲 PANGGIL TEKNISI SEKARANG"):
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

        st.success("Order berhasil dibuat. Silakan lanjutkan ke WhatsApp.")
        st.markdown(f"### [➡ HUBUNGI TEKNISI JONI]({link})")
    else:
        st.warning("Mohon isi nama, nomor HP, alamat, dan keluhan dulu.")

st.markdown("---")
st.caption("© GOBENG - Bengkel Panggilan Online")
