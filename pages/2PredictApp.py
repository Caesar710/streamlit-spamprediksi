#Import Library yang dibutuhkan
import streamlit as st
import string
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import joblib
import base64
from nltk.stem.snowball import PorterStemmer
ps = PorterStemmer()

# Input model dan vektorizer tfidf yang sudah disave
model = joblib.load('ModelSVM.pkl')
tfidf = joblib.load('TFIDF.pkl')

#Preprocessing
def text_preprocessing(text):
    
    # Case folding
    text = text.lower()
    
    # Data Cleaning
    text = text.replace("\n", " ")
    text = text.replace('\d+(\.\d+)?', 'numbers')
    text = text.replace(r'^.+@[^\.].*\.[a-z]{2,}$', 'MailID')
    text = text.replace(r'^http\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/\S*)?$', 'Links')
    text = text.replace('£', 'Money').replace('$', 'Money')
    text = text.replace('\s+', ' ')
    text = text.strip()
    text = text.replace(r'^\(?[\d]{3}\)?[\s-]?[\d]{3}[\s-]?[\d]{4}$', 'contact number')
    text = text.replace('![alt_text](image_url)', '')
    
    # Tokenizing
    text = nltk.word_tokenize(text)
    
    # Menghapus karakter khusus
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    text = y[:]
    y.clear()
    
    # Stopwords 
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
    text = y[:]
    y.clear()
    
    # Stemming
    stemmer = PorterStemmer()
    for i in text:
        y.append(stemmer.stem(i))
    
    return " ".join(y)

# Fungsi untuk membaca file yang diinput
def read_uploaded_file(uploaded_file):
    content = uploaded_file.getvalue().decode("utf-8")
    return content

# Fungsi untuk mengklasifikasikan email sebagai spam atau ham
def classify_text(text):
    # Preprocess Teks
    preprocessed_text = text_preprocessing(text)

    # Mengubah teks menggunakan vektorizer
    vectorized_text = tfidf.transform([preprocessed_text])

    # Membuat prediksi menggunakan model
    prediction = model.predict(vectorized_text)[0]

    return prediction

# Mendefinisikan hasil prediksi
def get_result_message(prediction, file_name):
    if prediction == 0:
        result_msg = "Email ini merupakan HAM"
    else:
        result_msg = "Email ini merupakan SPAM"
    return result_msg

## Set Konfigurasi Aplikasi 
st.set_page_config(page_title="Predict App")

# Mendefinisikan path logo
logo_path = "UMRI.png"  # Ganti dengan path logo yang sesuai

# Membaca logo sebagai base64
with open(logo_path, "rb") as logo_file:
    logo_data = base64.b64encode(logo_file.read()).decode("utf-8")

## Membuat Halaman Utama
st.title("Spam Prediction App")
st.write("Unggah file dalam format **<span style='color:yellow'>.eml</span>** untuk prediksi Email",  unsafe_allow_html=True)

## Membuat Fungsi upload
uploaded_files = st.file_uploader("Upload file(s)", accept_multiple_files=True)

# Memulai animasi spinner
with st.spinner("Menganalisis email..."):
    # Mengunggah setidaknya 1 file untuk diprediksi
    if uploaded_files is not None and len(uploaded_files) > 0:
        result_data = []  # Daftar untuk menyimpan data hasil prediksi
        for uploaded_file in uploaded_files:
            # Mengambil nama file
            file_name = uploaded_file.name

            # Mengkonversi file yang diunggah menjadi string
            if uploaded_file.type == "text/plain":
                file_contents = uploaded_file.read().decode("utf-8")
            elif uploaded_file.type == "message/rfc822":
                file_contents = uploaded_file.read().decode("utf-8", errors="ignore")
            else:
                st.error(f"Tipe file tidak didukung: {uploaded_file.type}")
                continue

            # Fungsi Klasifikasi Text
            prediction = classify_text(file_contents)

            # Fungsi untuk menampilkan hasil prediksi
            result_msg = get_result_message(prediction, file_name)
            result_data.append({"Email": file_name, "Hasil Prediksi": result_msg})

        # Menghentikan animasi spinner
        st.spinner(None)

        # Menampilkan tabel hasil prediksi
        st.write("Hasil Prediksi:")
        df_result = pd.DataFrame(result_data)
        st.dataframe(df_result)
    else:
        # Menghentikan animasi spinner jika tidak ada file yang diunggah
        st.spinner(None)
    
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
    st.write("Prediksi aplikasi ini tidak 100% akurat karena terdapat keterbatasan pada dataset yang digunakan untuk melatih model. Dataset yang digunakan mungkin tidak mencakup semua variasi dan karakteristik dari kategori SPAM yang ada di dunia nyata. Sebagai hasilnya, model mungkin tidak memiliki pemahaman yang lengkap tentang seluruh kategori SPAM yang mungkin muncul dalam email. Hal ini dapat menyebabkan beberapa email yang seharusnya diklasifikasikan sebagai SPAM tetap terklasifikasikan sebagai HAM atau sebaliknya")
## Pertanyaan 3
with st.sidebar.expander("Format apa saja yang mendukung untuk prediksi?"):
    st.write("Format yang didukung untuk prediksi Spam Email adalah **<span style='color:green'>.eml</span>**", unsafe_allow_html=True)

# Footer di Sidebar
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