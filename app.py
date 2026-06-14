import streamlit as st
import urllib.parse
import streamlit.components.v1 as components

st.set_page_config(page_title="GOBENG", page_icon="🏍️", layout="centered")

NOMOR_WA = "628562287257"

st.title("🏍️ GOBENG")
st.subheader("Motor Mogok? GOBENG Aja!")
st.write("Layanan Tambal Ban & Bengkel Panggilan")
st.markdown("---")

nama = st.text_input("Nama Pelanggan")
hp = st.text_input("Nomor HP")
kendaraan = st.selectbox("Jenis Kendaraan", ["Motor", "Mobil"])
layanan = st.selectbox("Pilih Layanan", ["Tambal Ban", "Motor Mogok", "Ganti Oli", "Servis Ringan", "Isi Angin", "Ganti Busi", "Aki Soak"])
alamat = st.text_area("Alamat Lengkap")
patokan = st.text_input("Patokan Lokasi")

st.markdown("### 📍 Ambil Lokasi Otomatis")
components.html("""
<button onclick="getLocation()" style="font-size:18px;padding:12px;border-radius:10px;">
📍 Ambil Lokasi Saya
</button>
<p id="lokasi"></p>
<script>
function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition, showError);
  } else {
    document.getElementById("lokasi").innerHTML = "Browser tidak mendukung GPS.";
  }
}
function showPosition(position) {
  var lat = position.coords.latitude;
  var lon = position.coords.longitude;
  var link = "https://maps.google.com/?q=" + lat + "," + lon;
  document.getElementById("lokasi").innerHTML =
    "Salin link lokasi ini:<br><b>" + link + "</b>";
}
function showError(error) {
  document.getElementById("lokasi").innerHTML =
    "Lokasi gagal terbaca. Pastikan izin lokasi aktif.";
}
</script>
""", height=160)

link_lokasi = st.text_input("Tempel link lokasi dari tombol di atas")

keluhan = st.text_area("Keluhan Kendaraan")

harga = {
    "Tambal Ban": "Mulai Rp15.000",
    "Motor Mogok": "Mulai Rp30.000",
    "Ganti Oli": "Mulai Rp7.000 jasa saja",
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
