import streamlit as st
import pandas as pd

# Fungsi untuk memuat data berdasarkan jenis hewan dan kabupaten
def load_data(jenis_hewan, nama_kabupaten):
    file_name = f"{jenis_hewan.lower()}.csv"
    data = pd.read_csv(file_name)
    if nama_kabupaten != "Semua Kabupaten":
        data = data[data["nama_kabupaten_kota"] == nama_kabupaten]
    return data

# Sidebar untuk memilih jenis hewan dan kabupaten
jenis_hewan = st.sidebar.selectbox("Pilih Jenis Hewan", ["Sapi", "Kerbau", "Kambing", "Kuda"])

# Memuat data berdasarkan jenis hewan yang dipilih
data = load_data(jenis_hewan, "Semua Kabupaten")

# Sidebar untuk memilih kabupaten
nama_kabupaten_options = ["Semua Kabupaten"] + list(data["nama_kabupaten_kota"].unique())
nama_kabupaten = st.sidebar.selectbox("Pilih Kabupaten", nama_kabupaten_options)

# Sidebar untuk memilih tahun
st.sidebar.subheader("Pilih Tahun:")
selected_years = st.sidebar.checkbox("Semua Tahun", value=True)

if not selected_years:
    tahun_options = st.sidebar.multiselect("Tahun", data["tahun"].unique())

# Memuat data berdasarkan jenis hewan dan kabupaten yang dipilih
if nama_kabupaten != "Semua Kabupaten":
    data = load_data(jenis_hewan, nama_kabupaten)

# Filter data berdasarkan tahun dan kabupaten yang dipilih
if not selected_years:
    data = data[data["tahun"].isin(tahun_options)]

# Tampilkan data
st.title(f"Populasi {jenis_hewan}")

# Menampilkan data
st.write("Data yang Dimuat:")
st.write(data)

# Total populasi
total_populasi = data['jumlah_populasi'].sum()
st.write(f"Total Populasi {jenis_hewan}: {total_populasi}")

# Grafik (opsional)
st.subheader("Grafik Populasi")
st.bar_chart(data[['nama_kabupaten_kota', 'jumlah_populasi']].set_index('nama_kabupaten_kota'))

# Analisis atau visualisasi tambahan dapat ditambahkan di sini