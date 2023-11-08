import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# Membaca data dari berkas CSV
data_sapi = pd.read_csv('sapi.csv')
data_kerbau = pd.read_csv('kerbau.csv')
data_kambing = pd.read_csv('kambing.csv')
data_kuda = pd.read_csv('kuda.csv')

# Menambahkan kolom jenis ternak ke setiap data frame sumber
data_sapi['jenis_ternak'] = 'Sapi'
data_kerbau['jenis_ternak'] = 'Kerbau'
data_kambing['jenis_ternak'] = 'Kambing'
data_kuda['jenis_ternak'] = 'Kuda'

# Menggabungkan data-data tersebut
data_gabungan = pd.concat([data_sapi, data_kerbau, data_kambing, data_kuda], ignore_index=True)

st.title("Dashboard Populasi Hewan Ternak di Jawa Barat")

selected_tab = option_menu(
    menu_title=None,
    options=["Home", "Perbandingan"],
    icons=["home", "percentage"],
    orientation="horizontal",
)

if selected_tab == "Home":
    # Tampilkan jumlah kabupaten
    jumlah_kabupaten = data_gabungan['nama_kabupaten_kota'].nunique()
    st.subheader(f"Jumlah Kabupaten : {jumlah_kabupaten} Kabupaten/Kota")

    # Buat 4 kolom untuk menampilkan total populasi
    col1, col2, col3, col4 = st.columns(4)

    # Total populasi sapi
    with col1:
        st.write('Jumlah Sapi')
        total_populasi_sapi = data_sapi['jumlah_populasi'].sum()
        col1.subheader(f"{total_populasi_sapi:,.0f}")

    # Total populasi kambing
    with col2:
        st.write('Jumlah Kambing')
        total_populasi_kambing = data_kambing['jumlah_populasi'].sum()
        col2.subheader(f"{total_populasi_kambing:,.0f}")

    # Total populasi kuda
    with col3:
        st.write('Jumlah Kuda')
        total_populasi_kuda = data_kuda['jumlah_populasi'].sum()
        col3.subheader(f" {total_populasi_kuda:,.0f}")

    # Total populasi ayam pedaging
    with col4:
        st.write('Jumlah Kerbau')
        total_populasi_kerbau = data_kerbau['jumlah_populasi'].sum()
        col4.subheader(f"{total_populasi_kerbau:,.0f}")

    # Tentukan warna untuk setiap jenis ternak
    warna_ternak = {
        'Sapi': 'orange',
        'Kambing': 'blue',
        'Kuda': 'yellow',
        'Kerbau': 'green'
    }

    # Buat diagram batang vertikal dengan warna yang telah ditentukan dan ukuran yang lebih besar
    fig = px.bar(data_gabungan, x='jumlah_populasi', y='nama_kabupaten_kota', color='jenis_ternak',
                 color_discrete_map=warna_ternak, title='Populasi Ternak berdasarkan Kabupaten')

    # Atur ukuran diagram batang
    fig.update_layout(width=800, height=600)

    st.plotly_chart(fig)

elif selected_tab == "Perbandingan":
    import streamlit as st
    import pandas as pd
    import matplotlib.pyplot as plt


    # Fungsi untuk memuat data berdasarkan jenis hewan dan tahun
    def load_data(jenis_hewan, tahun):
        file_name = f"{jenis_hewan.lower()}.csv"
        data = pd.read_csv(file_name)
        if tahun and 'Semua Tahun' not in tahun:
            data = data[data['tahun'].isin(tahun)]  # Filter data berdasarkan tahun
        return data


    # Sidebar untuk memilih jenis hewan dan tahun
    jenis_hewan = st.sidebar.multiselect("Pilih Hewan untuk Dibandingkan", ["Sapi", "Kerbau", "Kambing", "Kuda"])

    if jenis_hewan:  # Check if jenis_hewan is not empty
        tahun_options = sorted(
            pd.concat([pd.read_csv(f"{jenis.lower()}.csv") for jenis in jenis_hewan])['tahun'].unique())
    else:
        tahun_options = ['Semua Tahun']

    tahun_options.insert(0, 'Semua Tahun')  # Menambahkan opsi "Semua Tahun" di awal
    tahun = st.sidebar.multiselect("Pilih Tahun", tahun_options)  # Mengubah menjadi multiselect

    # Memuat data berdasarkan jenis hewan dan tahun yang dipilih
    data = [load_data(jenis, tahun) for jenis in jenis_hewan]

    # Komparasi Populasi
    if len(data) > 1:
        st.title("Komparasi Populasi")

        # Menghitung total populasi tiap jenis hewan
        total_populasi = {jenis: data[jenis_hewan.index(jenis)]['jumlah_populasi'].sum() for jenis in jenis_hewan}

        # Membuat dataframe untuk menampilkan dalam bentuk kolom
        df_total_populasi = pd.DataFrame(total_populasi.items(), columns=['Jenis Hewan', 'Jumlah Populasi'])

        # Menampilkan jumlah masing-masing hewan dalam bentuk kolom
        kolom = st.columns(len(jenis_hewan))  # Membuat kolom sejumlah jenis hewan yang dipilih

        for i, jenis in enumerate(jenis_hewan):
            kolom[i].write(f"{jenis}:")
            kolom[i].subheader(f"{total_populasi[jenis]:,.0f}")

        # Membuat label dan nilai untuk diagram lingkaran
        labels = list(total_populasi.keys())
        sizes = list(total_populasi.values())

        # Membuat diagram lingkaran
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  # Memastikan lingkaran berbentuk lingkaran

        # Menampilkan diagram lingkaran
        st.pyplot(fig1)





