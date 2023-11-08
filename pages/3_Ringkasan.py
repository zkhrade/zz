import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="Populasi Ternak",
)

# Load data
data_dict = {
    'Sapi': pd.read_csv('sapi.csv'),
    'Kambing': pd.read_csv('kambing.csv'),
    'Kuda': pd.read_csv('kuda.csv'),
    'Kerbau': pd.read_csv('kerbau.csv')
}

# Sidebar
st.sidebar.title('Pengaturan')
selected_option = st.sidebar.selectbox('Pilih Jenis Ternak', list(data_dict.keys()))

# Memilih data berdasarkan pilihan
selected_data = data_dict[selected_option]
# Tampilkan diagram batang
st.title(f'Populasi {selected_option}')
st.write(f'Data Populasi {selected_option} di Jawa Barat')

# Tampilkan total populasi per tahun
total_populasi_per_tahun = selected_data.groupby('tahun')['jumlah_populasi'].sum()
st.bar_chart(total_populasi_per_tahun)

# Grafik Populasi Ternak
chart = alt.Chart(selected_data).mark_area(opacity=0.3).encode(
    x='tahun',
    y='jumlah_populasi',
    color='nama_kabupaten_kota'
)
st.subheader(f'Grafik Populasi {selected_option}')
st.altair_chart(chart, use_container_width=True)
9