import streamlit as st
import urllib.parse
from datetime import datetime
import pandas as pd
import os

st.set_page_config(page_title="GOBENG", page_icon="🏍️", layout="centered")

NOMOR_WA = "628562287257"
FILE_ORDER = "orders.csv"
PASSWORD_ADMIN = "joni123"

def simpan_order(data):
    df_baru = pd.DataFrame([data])
    if os.path.exists(FILE_ORDER):
        df_lama = pd.read_csv(FILE_ORDER)
        df = pd.concat([df_lama, df_baru], ignore_index=True)
    else:
        df = df_baru
    df.to_csv(FILE_ORDER, index=False)

st.markdown("""
<style>
.stApp { background: #f7f8fa; }
.block-container { max-width: 760px; padding-top: 25px; }
.hero {
    background: linear-gradient(135deg, #e60000, #ff4b4b);
    padding: 28px;
    border-radius: 22px;
    color: white;
    text-align: center;
    box-shadow: 0 8px 25px rgba(230,0,0,0.25);
}
.hero h1 { font-size: 42px; margin: 0; }
.card {
    background: white;
    padding: 18px;
    border-radius: 18px;
    margin-top: 16px;
    box-shadow: 0 5px 18px rgba(0,0,0,0.06);
    border: 1px solid #eeeeee;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🏍️ GOBENG</h1>
    <p>Bengkel Panggilan Online • Cepat • Praktis • Terpercaya</p>
</div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "Menu GOBENG",
    ["Pesan Layanan", "Dashboard Admin"]
)

harga = {
    "Tambal Ban": "Mulai Rp15.000",
    "Motor Mogok": "Mulai Rp20.000",
    "Ganti Oli": "Jasa mulai Rp5.000",
    "Servis Ringan": "Mulai Rp20.000",
    "Isi Angin": "Mulai Rp5.000",
    "Ganti Busi": "Jasa mulai Rp10.000",
    "Aki Soak": "Menyesuaikan kondisi kendaraan",
}

if menu == "Pesan Layanan":
    st.markdown("""
    <div class="card">
    <b>Motor mogok? Ban bocor?</b><br>
    GOBENG siap membantu Anda dengan teknisi panggilan langsung ke lokasi.
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

    st.success(f"Estimasi biaya: {harga[layanan]}")

    st.warning("""
    🚨 Biaya panggilan menyesuaikan jarak lokasi pelanggan.

    Estimasi final akan diinformasikan teknisi sebelum pengerjaan.
    """)

    st.info("Setelah WhatsApp terbuka, pelanggan bisa langsung mengirim share location kepada teknisi.")

    if st.button("📲 PANGGIL TEKNISI SEKARANG", use_container_width=True):
        if nama and hp and alamat and keluhan:
            order_id = "GB-" + datetime.now().strftime("%Y%m%d-%H%M%S")
            waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            status_foto = "Sudah upload foto kerusakan" if foto else "Belum upload foto"

            data_order = {
                "Order ID": order_id,
                "Waktu": waktu,
                "Nama": nama,
                "HP": hp,
                "Kendaraan": kendaraan,
                "Layanan": layanan,
                "Estimasi": harga[layanan],
                "Alamat": alamat,
                "Patokan": patokan,
                "Keluhan": keluhan,
                "Foto": status_foto,
                "Status": "Menunggu"
            }

            simpan_order(data_order)

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

            st.success(f"Order berhasil dibuat: {order_id}")
            st.markdown(f"### [➡ LANJUT KE WHATSAPP TEKNISI]({link})")
        else:
            st.warning("Mohon isi nama, nomor HP, alamat, dan keluhan dulu.")

if menu == "Dashboard Admin":
    st.markdown("### 🔐 Dashboard Admin GOBENG")
    password = st.text_input("Masukkan Password Admin", type="password")

    if password == PASSWORD_ADMIN:
        if os.path.exists(FILE_ORDER):
            df = pd.read_csv(FILE_ORDER)

            st.success("Login admin berhasil.")

            total_order = len(df)
            menunggu = len(df[df["Status"] == "Menunggu"])

            col1, col2 = st.columns(2)
            col1.metric("Total Order", total_order)
            col2.metric("Order Menunggu", menunggu)

            st.markdown("### 📋 Riwayat Order")
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download Data Order",
                data=csv,
                file_name="riwayat_order_gobeng.csv",
                mime="text/csv"
            )
        else:
            st.info("Belum ada order masuk.")
    elif password:
        st.error("Password salah.")

st.markdown("---")
st.caption("© GOBENG - Bengkel Panggilan Online")
