import streamlit as st
import urllib.parse
from datetime import datetime
import pandas as pd
import os

st.set_page_config(page_title="GOBENG V3", page_icon="🏍️", layout="centered")

NOMOR_WA_JONI = "628562287257"
NOMOR_WA_OWNER = "6281395440454"
FILE_ORDER = "orders.csv"
PASSWORD_ADMIN = "joni123"

harga = {
    "Tambal Ban": "Mulai Rp15.000",
    "Motor Mogok": "Mulai Rp20.000",
    "Ganti Oli": "Jasa mulai Rp5.000",
    "Servis Ringan": "Mulai Rp20.000",
    "Isi Angin": "Mulai Rp5.000",
    "Ganti Busi": "Jasa mulai Rp10.000",
    "Aki Soak": "Menyesuaikan kondisi kendaraan",
}

def ongkos_panggilan(jarak):
    if jarak <= 3:
        return "Gratis panggilan"
    elif jarak <= 5:
        return "Rp5.000"
    elif jarak <= 10:
        return "Rp10.000"
    else:
        return "Menyesuaikan jarak"

def simpan_order(data):
    df_baru = pd.DataFrame([data])
    if os.path.exists(FILE_ORDER):
        df_lama = pd.read_csv(FILE_ORDER)
        df = pd.concat([df_lama, df_baru], ignore_index=True)
    else:
        df = df_baru
    df.to_csv(FILE_ORDER, index=False)

def update_status(order_id, status_baru):
    if os.path.exists(FILE_ORDER):
        df = pd.read_csv(FILE_ORDER)
        df.loc[df["Order ID"] == order_id, "Status"] = status_baru
        df.to_csv(FILE_ORDER, index=False)

st.markdown("""
<style>
.stApp { background: #f6f7fb; }
.block-container { max-width: 820px; padding-top: 25px; }
.hero {
    background: linear-gradient(135deg, #d90000, #ff3b3b);
    padding: 30px;
    border-radius: 24px;
    color: white;
    text-align: center;
    box-shadow: 0 10px 28px rgba(230,0,0,0.25);
}
.hero h1 { font-size: 44px; margin: 0; }
.hero p { font-size: 17px; margin-top: 8px; }
.card {
    background: white;
    padding: 18px;
    border-radius: 18px;
    margin-top: 16px;
    box-shadow: 0 5px 18px rgba(0,0,0,0.06);
    border: 1px solid #eeeeee;
}
.danger {
    background: #111111;
    color: white;
    padding: 18px;
    border-radius: 18px;
    margin-top: 16px;
    text-align: center;
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
    <h1>🏍️ GOBENG V3</h1>
    <p>Bengkel Panggilan Online • Cepat • Praktis • Terpercaya</p>
</div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "Menu GOBENG",
    ["Pesan Layanan", "Dashboard Admin"]
)

if menu == "Pesan Layanan":
    st.markdown("""
    <div class="card">
    <b>Motor mogok? Ban bocor?</b><br>
    GOBENG siap membantu Anda dengan teknisi panggilan langsung ke lokasi.
    </div>
    """, unsafe_allow_html=True)

    pesan_darurat = """
Halo GOBENG

Saya butuh bantuan DARURAT.

Motor mogok / kendaraan bermasalah.
Mohon teknisi Joni segera merespons.

Saya akan kirim lokasi lewat WhatsApp.
"""
    link_darurat = f"https://wa.me/{NOMOR_WA_JONI}?text={urllib.parse.quote(pesan_darurat)}"

    st.markdown(f"""
    <div class="danger">
    <h3>🚨 Darurat Motor Mogok?</h3>
    <p>Klik tombol di bawah untuk langsung menghubungi teknisi.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"### [🚨 HUBUNGI JONI SEKARANG]({link_darurat})")

    st.markdown("### 📞 Bantuan & Pengaduan")
    st.info("""
👨‍🔧 Teknisi Lapangan: Joni — 0856-2287-257  
👨‍💼 Bantuan / Owner GOBENG: 0813-9544-0454
""")

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
    layanan = st.selectbox("Pilih Layanan", list(harga.keys()))
    jarak = st.number_input("Perkiraan Jarak dari Teknisi/Bengkel (KM)", min_value=0.0, step=0.5)

    alamat = st.text_area("Alamat Lengkap")
    patokan = st.text_input("Patokan Lokasi")
    keluhan = st.text_area("Keluhan Kendaraan")

    foto = st.file_uploader("Upload Foto Kerusakan Kendaraan", type=["jpg", "jpeg", "png"])
    if foto:
        st.image(foto, caption="Foto kerusakan berhasil diupload", use_container_width=True)

    biaya_panggilan = ongkos_panggilan(jarak)

    st.success(f"Estimasi jasa: {harga[layanan]}")
    st.info(f"Estimasi ongkos panggilan: {biaya_panggilan}")
    st.warning("Estimasi final akan diinformasikan teknisi sebelum pengerjaan.")
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
                "Jarak KM": jarak,
                "Estimasi Jasa": harga[layanan],
                "Ongkos Panggilan": biaya_panggilan,
                "Alamat": alamat,
                "Patokan": patokan,
                "Keluhan": keluhan,
                "Foto": status_foto,
                "Status": "Menunggu Teknisi"
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
Estimasi Jasa: {harga[layanan]}
Perkiraan Jarak: {jarak} KM
Ongkos Panggilan: {biaya_panggilan}
Alamat: {alamat}
Patokan: {patokan}
Keluhan: {keluhan}
Foto Kerusakan: {status_foto}

Catatan:
Saya akan mengirim share location lewat WhatsApp setelah ini.

Mohon bantuan teknisi Joni datang ke lokasi.
"""
            link_joni = f"https://wa.me/{NOMOR_WA_JONI}?text={urllib.parse.quote(pesan)}"
            link_owner = f"https://wa.me/{NOMOR_WA_OWNER}?text={urllib.parse.quote('Salinan order GOBENG:\\n' + pesan)}"

            st.success(f"Order berhasil dibuat: {order_id}")
            st.markdown(f"### [➡ KIRIM ORDER KE JONI]({link_joni})")
            st.markdown(f"### [📩 KIRIM SALINAN KE OWNER]({link_owner})")
        else:
            st.warning("Mohon isi nama, nomor HP, alamat, dan keluhan dulu.")

if menu == "Dashboard Admin":
    st.markdown("### 🔐 Dashboard Admin GOBENG V3")
    password = st.text_input("Masukkan Password Admin", type="password")

    if password == PASSWORD_ADMIN:
        st.success("Login admin berhasil.")

        if os.path.exists(FILE_ORDER):
            df = pd.read_csv(FILE_ORDER)

            total_order = len(df)
            menunggu = len(df[df["Status"] == "Menunggu Teknisi"])
            berangkat = len(df[df["Status"] == "Teknisi Berangkat"])
            dikerjakan = len(df[df["Status"] == "Sedang Dikerjakan"])
            selesai = len(df[df["Status"] == "Selesai"])

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total", total_order)
            col2.metric("Menunggu", menunggu)
            col3.metric("Berangkat", berangkat)
            col4.metric("Selesai", selesai)

            st.markdown("### 🔄 Ubah Status Order")
            order_pilih = st.selectbox("Pilih Order ID", df["Order ID"].tolist())
            status_baru = st.selectbox(
                "Status Baru",
                ["Menunggu Teknisi", "Teknisi Berangkat", "Sedang Dikerjakan", "Selesai", "Batal"]
            )

            if st.button("Simpan Status"):
                update_status(order_pilih, status_baru)
                st.success(f"Status {order_pilih} diubah menjadi {status_baru}. Silakan refresh halaman.")

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
