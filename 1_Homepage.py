# Import Library yang dibutuhkan
import streamlit as st
from PIL import Image
import base64

# Mendefinisikan path logo
logo_path = "UMRI.png"  # Ganti dengan path logo yang sesuai

# Membaca logo sebagai base64
with open(logo_path, "rb") as logo_file:
    logo_data = base64.b64encode(logo_file.read()).decode("utf-8")

# Membuat konfigurasi halaman
st.set_page_config(page_title="Homepage")

## Membuat Halaman Utama
st.title("Spam Prediction App")
st.markdown(
    """
    Aplikasi ini dirancang untuk membantu mendeteksi apakah sebuah email masuk ke dalam kategori <span style='color:red'>SPAM</span> atau <span style='color:green'>HAM</span>. 
    File yang dapat diunggah email dalam format <span style='color:yellow'>.eml</span>, dan aplikasi akan menggunakan model machine learning yang sudah dibangun menggunakan algoritma <span style='color:blue'>SVM</span> untuk melakukan prediksi.
    
    ### Tentang Aplikasi
    - Dataset yang digunakan diambil dari [Kaggle](https://www.kaggle.com/)
    - Email Spam Dataset [Ling-Spam Dataset](https://www.kaggle.com/datasets/mandygu/lingspam-dataset)
    - Menggunakan Algoritma Support Vector Machine
    - Merupakan bagian dari tugas akhir skripsi
    """
, unsafe_allow_html=True)

st.markdown("---")

# Membuat Sidebar
st.sidebar.title("FAQ")

#Pertanyaan 1
with st.sidebar.expander("Bagaimana Aplikasi dapat bekerja?"):
    st.write("1. Pengguna mengunggah file email dalam format **<span style='color:yellow'>.eml</span>** melalui antarmuka aplikasi.",unsafe_allow_html=True)
    st.write("2. Aplikasi mengkonversi konten file email menjadi teks yang dapat diproses.")
    st.write("3. Sebelum model melakukan prediksi, Dilakukan tahap preprocessing pada teks email untuk membersihkan dan mengubahnya menjadi format yang sesuai.")
    st.write("4. Teks email kemudian diberikan kepada model machine learning yang sudah dibangun sebelumnya.")
    st.write("5. Model melakukan prediksi apakah email tersebut termasuk dalam kategori **<span style='color:red'>SPAM</span>** atau **<span style='color:green'>HAM</span>**",unsafe_allow_html=True)
    st.write("6. Hasil prediksi ditampilkan kepada pengguna dalam bentuk yang dapat dibaca.")
## Pertanyaan 2
with st.sidebar.expander("Apakah aplikasi ini 100% Akurat?"):
    st.write("Prediksi aplikasi ini tidak 100% akurat karena terdapat keterbatasan pada dataset yang digunakan untuk melatih model. Dataset yang digunakan mungkin tidak mencakup semua variasi dan karakteristik dari kategori **<span style='color:red'>SPAM</span>** yang ada di dunia nyata. Sebagai hasilnya, model mungkin tidak memiliki pemahaman yang lengkap tentang seluruh kategori **<span style='color:red'>SPAM</span>** yang mungkin muncul dalam email. Hal ini dapat menyebabkan beberapa email yang seharusnya diklasifikasikan sebagai **<span style='color:red'>SPAM</span>** tetap terklasifikasikan sebagai **<span style='color:green'>HAM</span>** atau sebaliknya", unsafe_allow_html=True)
## Pertanyaan 3
with st.sidebar.expander("Format apa saja yang mendukung untuk prediksi?"):
    st.write("Format yang didukung untuk prediksi Spam Email adalah **<span style='color:green'>.eml</span>**", unsafe_allow_html=True)

st.sidebar.markdown(
    """
    <style>
    .sidebar-footer {
        margin-top: auto;
        color: #FAFAFA;
        padding: 10px;
        background-color: #262730;
        text-align: center;
        font-size: 12px;
    }
    </style>
    """
    "<div class='sidebar-footer'>"
    "Dibuat oleh M Hafiz Caesar"
    "</div>",
    unsafe_allow_html=True
)

# Menampilkan footer dengan logo
st.markdown(
    f"""
    <style>
    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        color: #FAFAFA;
        padding: 10px;
        background-color: #0E1117;
    }}
    .footer-logo {{
        display: flex;
        justify-content: center;
        align-items: center;
    }}
    .footer-logo img {{
        width: 50px;
        height: 50px;
        object-fit: contain;
        margin-right: 10px;
    }}
    </style>
    <div class="footer">
        <div class="footer-logo">
            <img src="data:image/png;base64,{logo_data}" alt="Logo">
            © 2023 M Hafiz Caesar, Teknik Informatika, Universitas Muhammadiyah Riau. All rights reserved.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)