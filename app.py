import streamlit as st
import urllib.parse

st.set_page_config(page_title="GOBENG", page_icon="🏍️", layout="centered")

NOMOR_WA = "628562287257"

st.title("🏍️ GOBENG")
st.subheader("Motor Mogok? GOBENG Aja!")
st.write("Layanan Tambal Ban & Bengkel Panggilan")
st.markdown("---")

nama = st.text_input("Nama Pelanggan")
hp = st.text_input("Nomor HP")
kendaraan = st.selectbox("Jenis Kendaraan", ["Motor", "Mobil"])

layanan = st.selectbox(
    "Pilih Layanan",
    ["Tambal Ban", "Motor Mogok", "Ganti Oli", "Servis Ringan", "Isi Angin", "Ganti Busi", "Aki Soak"]
)

alamat = st.text_area("Alamat Lengkap")
patokan = st.text_input("Patokan Lokasi")
keluhan = st.text_area("Keluhan Kendaraan")

foto = st.file_uploader(
    "Upload foto kerusakan kendaraan",
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

st.info(f"Estimasi biaya: {harga[layanan]}")

st.info("Untuk lokasi, pelanggan bisa kirim share location langsung di WhatsApp setelah tombol dibuka.")

if st.button("📲 Panggil Teknisi Joni"):
    if nama and hp and alamat and keluhan:
        status_foto = "Sudah upload foto kerusakan" if foto else "Belum upload foto"

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
Keluhan: {keluhan}
Foto Kerusakan: {status_foto}

Catatan:
Saya akan mengirim share location lewat WhatsApp setelah ini.

Mohon bantuan teknisi Joni datang ke lokasi.
"""
        link = f"https://wa.me/{NOMOR_WA}?text={urllib.parse.quote(pesan)}"

        st.success("Data siap dikirim ke WhatsApp Teknisi Joni.")
        st.markdown(f"### [➡ Hubungi Teknisi Joni]({link})")
    else:
        st.warning("Mohon isi nama, nomor HP, alamat, dan keluhan dulu.")

st.markdown("---")
st.caption("GOBENG - Bengkel Panggilan Online")
