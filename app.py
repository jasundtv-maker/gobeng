import streamlit as st
import urllib.parse
from streamlit_js_eval import get_geolocation

st.set_page_config(
    page_title="GOBENG",
    page_icon="🏍️",
    layout="centered"
)

NOMOR_WA = "628562287257"

st.title("🏍️ GOBENG")
st.subheader("Motor Mogok? GOBENG Aja!")
st.write("Layanan Tambal Ban & Bengkel Panggilan")

st.markdown("---")

nama = st.text_input("Nama Pelanggan")
hp = st.text_input("Nomor HP")

kendaraan = st.selectbox(
    "Jenis Kendaraan",
    ["Motor", "Mobil"]
)

layanan = st.selectbox(
    "Pilih Layanan",
    [
        "Tambal Ban",
        "Motor Mogok",
        "Ganti Oli",
        "Servis Ringan",
        "Isi Angin",
        "Ganti Busi",
        "Aki Soak"
    ]
)

alamat = st.text_area("Alamat Lengkap")
patokan = st.text_input("Patokan Lokasi")

st.markdown("### 📍 Lokasi Pelanggan")
st.info("Klik tombol di bawah, lalu izinkan akses lokasi. Link Google Maps akan otomatis dibuat.")

lokasi_link = ""

if st.button("📍 Ambil Lokasi Saya"):
    lokasi = get_geolocation()

    if lokasi:
        lat = lokasi["coords"]["latitude"]
        lon = lokasi["coords"]["longitude"]
        lokasi_link = f"https://maps.google.com/?q={lat},{lon}"

        st.session_state["lokasi_link"] = lokasi_link
        st.success("Lokasi berhasil didapatkan.")
        st.write(lokasi_link)
    else:
        st.warning("Lokasi belum terbaca. Pastikan izin lokasi di browser sudah diaktifkan.")

if "lokasi_link" not in st.session_state:
    st.session_state["lokasi_link"] = ""

link_lokasi = st.session_state["lokasi_link"]

keluhan = st.text_area("Keluhan Kendaraan")

harga = {
    "Tambal Ban": "Mulai Rp15.000",
    "Motor Mogok": "Mulai Rp30.000",
    "Ganti Oli": "Mulai Rp20.000 jasa saja",
    "Servis Ringan": "Mulai Rp35.000",
    "Isi Angin": "Mulai Rp5.000",
    "Ganti Busi": "Mulai Rp15.000 jasa saja",
    "Aki Soak": "Mulai Rp30.000",
}

st.info(f"Estimasi biaya: {harga[layanan]}")

if st.button("📲 Panggil Teknisi Joni"):
    if nama and hp and alamat and keluhan:
        pesan = f"""
Halo GOBENG

Saya ingin panggil teknisi.

Nama: {nama}
No HP: {hp}
Jenis Kendaraan: {kendaraan}
Layanan: {layanan}
Estimasi Biaya: {harga[layanan]}
Alamat: {alamat}
Patokan: {patokan}
Lokasi Google Maps: {link_lokasi}
Keluhan: {keluhan}

Mohon bantuan teknisi Joni datang ke lokasi.
"""
        link = f"https://wa.me/{NOMOR_WA}?text={urllib.parse.quote(pesan)}"

        st.success("Data siap dikirim ke WhatsApp Teknisi Joni.")
        st.markdown(f"### [➡ Hubungi Teknisi Joni]({link})")
    else:
        st.warning("Mohon isi nama, nomor HP, alamat, dan keluhan dulu.")

st.markdown("---")
st.caption("GOBENG - Bengkel Panggilan Online")
