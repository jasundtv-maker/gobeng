import streamlit as st
import urllib.parse
from datetime import datetime
import pandas as pd
import os
import requests

st.set_page_config(page_title="GOBENG V7", page_icon="🏍️", layout="centered")

NOMOR_WA_JONI = "628562287257"
NOMOR_WA_OWNER = "6281395440454"

BOT_TOKEN = "8742663611:AAE4hrUYrM8gagxr9qQCPd2N71TH9czF3tY"
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
        if "Biaya Final" not in df.columns:
            df["Biaya Final"] = 0
        if "Rating" not in df.columns:
            df["Rating"] = 0
        if "Ulasan" not in df.columns:
            df["Ulasan"] = ""

        df["Ulasan"] = df["Ulasan"].astype("object")

        df.loc[df["Order ID"] == order_id, "Status"] = status_baru
        df.loc[df["Order ID"] == order_id, "Biaya Final"] = int(biaya_final)
        df.loc[df["Order ID"] == order_id, "Rating"] = int(rating)
        df.loc[df["Order ID"] == order_id, "Ulasan"] = str(ulasan)
        df.to_csv(FILE_ORDER, index=False)

def kirim_telegram(pesan):
    if BOT_TOKEN and CHAT_ID_OWNER:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            data = {
                "chat_id": CHAT_ID_OWNER,
                "text": pesan,
                "parse_mode": "HTML"
            }
            requests.post(url, data=data, timeout=10)
        except Exception:
            pass

st.markdown("""
<style>
.stApp { background: #f6f7fb; }
.block-container { max-width: 850px; padding-top: 25px; }
.hero {
    background: linear-gradient(135deg, #d60000, #ff4040);
    padding: 30px;
    border-radius: 24px;
    color: white;
    text-align: center;
    box-shadow: 0 10px 28px rgba(230,0,0,0.25);
}
.hero h1 { font-size: 44px; margin: 0; }
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
    <p>Bengkel Panggilan Online • Cepat • Aman • Terpercaya</p>
</div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio("Menu GOBENG", ["Pesan Layanan", "Dashboard Admin"])

if menu == "Pesan Layanan":
    st.markdown("""
<div class="card">
<b>Motor mogok? Ban bocor?</b><br>
Pilih Pesan Cepat kalau ingin langsung panggil teknisi.
</div>
""", unsafe_allow_html=True)

    st.info("""
👨‍🔧 Teknisi Joni: 0856-2287-257  
👨‍💼 Bantuan Owner: 0813-9544-0454
""")

    mode = st.radio("Pilih Cara Pesan", ["🟢 Pesan Cepat", "🔵 Pesan Lengkap"])

    if mode == "🟢 Pesan Cepat":
        st.markdown("### 🟢 Pesan Cepat")

        nama = st.text_input("Nama")
        hp = st.text_input("Nomor WhatsApp")
        layanan = st.selectbox("Pilih Layanan", list(harga.keys()))
        lokasi = st.text_input("Link Google Maps / Share Location")
        catatan = st.text_area("Catatan singkat, contoh: ban kempes di jalan")

        st.success(f"Estimasi jasa: {harga[layanan]}")
        st.warning("Biaya panggilan menyesuaikan jarak lokasi pelanggan.")

        if st.button("📲 PANGGIL TEKNISI SEKARANG", use_container_width=True):
            if nama and hp and layanan:
                order_id = "GB-" + datetime.now().strftime("%Y%m%d-%H%M%S")
                waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                data_order = {
                    "Order ID": order_id,
                    "Waktu": waktu,
                    "Nama": nama,
                    "HP": hp,
                    "Kendaraan": "Motor",
                    "Layanan": layanan,
                    "Jarak KM": "",
                    "Estimasi Jasa": harga[layanan],
                    "Ongkos Panggilan": "Menyesuaikan lokasi",
                    "Alamat": "",
                    "Patokan": "",
                    "Keluhan": catatan,
                    "Foto": "Tidak ada foto",
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
Layanan: {layanan}
Estimasi Jasa: {harga[layanan]}
Lokasi Google Maps: {lokasi}
Catatan: {catatan}

Mohon bantuan teknisi Joni datang ke lokasi.
"""

                telegram_msg = f"""
🔔 ORDER BARU GOBENG

Order ID: {order_id}
Nama: {nama}
HP: {hp}
Layanan: {layanan}
Lokasi: {lokasi}
Catatan: {catatan}
Status: Menunggu Teknisi
"""
                kirim_telegram(telegram_msg)

                link_joni = f"https://wa.me/{NOMOR_WA_JONI}?text={urllib.parse.quote(pesan)}"
                st.success(f"Order berhasil dibuat: {order_id}")
                st.markdown(f"### [➡ KIRIM ORDER KE JONI]({link_joni})")
            else:
                st.warning("Mohon isi nama dan nomor WhatsApp dulu.")

    if mode == "🔵 Pesan Lengkap":
        st.markdown("### 🔵 Pesan Lengkap")

        nama = st.text_input("Nama Pelanggan")
        hp = st.text_input("Nomor HP / WhatsApp")
        kendaraan = st.selectbox("Jenis Kendaraan", ["Motor", "Mobil"])
        layanan = st.selectbox("Pilih Layanan", list(harga.keys()))
        jarak = st.number_input("Perkiraan Jarak dari Bengkel (KM)", min_value=0.0, step=0.5)

        alamat = st.text_area("Alamat Lengkap")
        patokan = st.text_input("Patokan Lokasi")
        link_maps = st.text_input("Link Google Maps / Share Location")
        keluhan = st.text_area("Keluhan Kendaraan")

        foto = st.file_uploader("Upload Foto Kerusakan Kendaraan", type=["jpg", "jpeg", "png"])
        if foto:
            st.image(foto, caption="Foto kerusakan berhasil diupload", use_container_width=True)

        biaya_panggilan = ongkos_panggilan(jarak)

        st.success(f"Estimasi jasa: {harga[layanan]}")
        st.info(f"Estimasi ongkos panggilan: {biaya_panggilan}")
        st.warning("Estimasi final akan diinformasikan teknisi sebelum pengerjaan.")

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
Google Maps: {link_maps}
Keluhan: {keluhan}
Foto Kerusakan: {status_foto}

Mohon bantuan teknisi Joni datang ke lokasi.
"""

                telegram_msg = f"""
🔔 ORDER BARU GOBENG

Order ID: {order_id}
Nama: {nama}
HP: {hp}
Layanan: {layanan}
Alamat: {alamat}
Patokan: {patokan}
Google Maps: {link_maps}
Keluhan: {keluhan}
Status: Menunggu Teknisi
"""
                kirim_telegram(telegram_msg)

                link_joni = f"https://wa.me/{NOMOR_WA_JONI}?text={urllib.parse.quote(pesan)}"
                link_owner = f"https://wa.me/{NOMOR_WA_OWNER}?text={urllib.parse.quote('Salinan order GOBENG:\\n' + pesan)}"

                st.success(f"Order berhasil dibuat: {order_id}")
                st.markdown(f"### [➡ KIRIM ORDER KE JONI]({link_joni})")
                st.markdown(f"### [📩 KIRIM SALINAN KE OWNER]({link_owner})")
            else:
                st.warning("Mohon isi nama, nomor HP, alamat, dan keluhan dulu.")

if menu == "Dashboard Admin":
    st.markdown("### 🔐 Dashboard Admin GOBENG")
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
            selesai = len(df[df["Status"] == "Selesai"])
            pendapatan = int(pd.to_numeric(df["Biaya Final"], errors="coerce").fillna(0).sum())

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Order", total_order)
            col2.metric("Selesai", selesai)
            col3.metric("Pendapatan", f"Rp{pendapatan:,.0f}".replace(",", "."))

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
