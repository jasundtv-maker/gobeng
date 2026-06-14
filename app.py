import streamlit as st
import urllib.parse
from datetime import datetime
import pandas as pd
import os
import requests

st.set_page_config(page_title="GOBENG V5", page_icon="🏍️", layout="centered")

NOMOR_WA_JONI = "628562287257"
NOMOR_WA_OWNER = "6281395440454"

BOT_TOKEN = "8742663611:AAFxqT7hOaBXgxex1Bkn4mnM40zPWp_eLO8"
CHAT_ID_OWNER = "8951538688"

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
    return "Menyesuaikan jarak"

def kirim_telegram(pesan):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": CHAT_ID_OWNER,
            "text": pesan
        }
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        print("Gagal kirim Telegram:", e)

def simpan_order(data):
    df_baru = pd.DataFrame([data])
    if os.path.exists(FILE_ORDER):
        df_lama = pd.read_csv(FILE_ORDER)
        df = pd.concat([df_lama, df_baru], ignore_index=True)
    else:
        df = df_baru
    df.to_csv(FILE_ORDER, index=False)

def baca_order():
    if os.path.exists(FILE_ORDER):
        return pd.read_csv(FILE_ORDER)
    return pd.DataFrame()

def update_order(order_id, status_baru, biaya_final, rating, ulasan):
    df = baca_order()
    if not df.empty:
        df.loc[df["Order ID"] == order_id, "Status"] = status_baru
        df.loc[df["Order ID"] == order_id, "Biaya Final"] = biaya_final
        df.loc[df["Order ID"] == order_id, "Rating"] = rating
        df.loc[df["Order ID"] == order_id, "Ulasan"] = ulasan
        df.to_csv(FILE_ORDER, index=False)

st.markdown("""
<style>
.stApp { background: #f5f6fa; }
.block-container { max-width: 850px; padding-top: 25px; }
.hero {
    background: linear-gradient(135deg, #d60000, #ff4040);
    padding: 32px;
    border-radius: 26px;
    color: white;
    text-align: center;
    box-shadow: 0 10px 30px rgba(230,0,0,0.25);
}
.hero h1 { font-size: 46px; margin: 0; }
.hero p { font-size: 18px; margin-top: 8px; }
.card {
    background: white;
    padding: 18px;
    border-radius: 18px;
    margin-top: 16px;
    box-shadow: 0 5px 18px rgba(0,0,0,0.06);
    border: 1px solid #eeeeee;
}
.service {
    background: #fff4f4;
    padding: 12px;
    border-radius: 14px;
    margin: 6px 0;
    border: 1px solid #ffd0d0;
}
.danger {
    background: #111;
    color: white;
    padding: 18px;
    border-radius: 18px;
    text-align: center;
    margin-top: 16px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🏍️ GOBENG V5</h1>
    <p>Bengkel Panggilan Online • Cepat • Praktis • Terpercaya</p>
</div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio("Menu GOBENG", ["Pesan Layanan", "Dashboard Admin"])

if menu == "Pesan Layanan":
    st.success("🔥 Promo GOBENG: Tambal ban mulai Rp15.000. Biaya panggilan menyesuaikan jarak.")

    st.markdown("""
<div class="card">
<b>Kenapa pilih GOBENG?</b><br>
⭐ Rating pelayanan 4.9<br>
⚡ Respon cepat<br>
📍 Datang ke lokasi pelanggan<br>
🔧 Teknisi berpengalaman<br>
🔔 Owner menerima notifikasi Telegram otomatis
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

    st.markdown("""
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
                "Status": "Menunggu Teknisi",
                "Biaya Final": 0,
                "Rating": 0,
                "Ulasan": ""
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

            notif_telegram = f"""
🔔 ORDER BARU GOBENG

🆔 Order ID: {order_id}
⏰ Waktu: {waktu}

👤 Nama: {nama}
📱 HP/WA: {hp}
🏍️ Kendaraan: {kendaraan}
🔧 Layanan: {layanan}

💰 Estimasi Jasa: {harga[layanan]}
📍 Jarak: {jarak} KM
🚚 Ongkos Panggilan: {biaya_panggilan}

🏠 Alamat:
{alamat}

📌 Patokan:
{patokan}

🛠️ Keluhan:
{keluhan}

📷 Foto: {status_foto}

Status: Menunggu Teknisi
"""

            kirim_telegram(notif_telegram)

            link_joni = f"https://wa.me/{NOMOR_WA_JONI}?text={urllib.parse.quote(pesan)}"
            link_owner = f"https://wa.me/{NOMOR_WA_OWNER}?text={urllib.parse.quote('Salinan order GOBENG:\\n' + pesan)}"

            st.success(f"Order berhasil dibuat: {order_id}")
            st.success("Notifikasi Telegram otomatis dikirim ke Owner.")
            st.markdown(f"### [➡ KIRIM ORDER KE JONI]({link_joni})")
            st.markdown(f"### [📩 KIRIM SALINAN KE OWNER]({link_owner})")
        else:
            st.warning("Mohon isi nama, nomor HP, alamat, dan keluhan dulu.")

if menu == "Dashboard Admin":
    st.markdown("### 🔐 Dashboard Admin GOBENG V5")
    password = st.text_input("Masukkan Password Admin", type="password")

    if password == PASSWORD_ADMIN:
        st.success("Login admin berhasil.")
        df = baca_order()

        if not df.empty:
            if "Biaya Final" not in df.columns:
                df["Biaya Final"] = 0
            if "Rating" not in df.columns:
                df["Rating"] = 0
            if "Ulasan" not in df.columns:
                df["Ulasan"] = ""

            total_order = len(df)
            order_hari_ini = len(df[df["Waktu"].astype(str).str.startswith(datetime.now().strftime("%Y-%m-%d"))])
            selesai = len(df[df["Status"] == "Selesai"])
            pendapatan = int(pd.to_numeric(df["Biaya Final"], errors="coerce").fillna(0).sum())
            rata_rating = pd.to_numeric(df["Rating"], errors="coerce").replace(0, pd.NA).dropna().mean()

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Order", total_order)
            col2.metric("Order Hari Ini", order_hari_ini)
            col3.metric("Selesai", selesai)
            col4.metric("Pendapatan", f"Rp{pendapatan:,.0f}".replace(",", "."))

            if pd.notna(rata_rating):
                st.success(f"⭐ Rating rata-rata: {rata_rating:.1f}/5")

            st.markdown("### 🔄 Update Order")
            order_pilih = st.selectbox("Pilih Order ID", df["Order ID"].tolist())
            status_baru = st.selectbox(
                "Status Baru",
                ["Menunggu Teknisi", "Teknisi Berangkat", "Sedang Dikerjakan", "Selesai", "Batal"]
            )
            biaya_final = st.number_input("Total Tagihan / Biaya Final", min_value=0, step=1000)
            rating = st.slider("Rating Pelanggan", 0, 5, 0)
            ulasan = st.text_area("Ulasan Pelanggan")

            if st.button("Simpan Update Order", use_container_width=True):
                update_order(order_pilih, status_baru, biaya_final, rating, ulasan)
                st.success("Update order berhasil. Refresh halaman untuk melihat perubahan.")

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
