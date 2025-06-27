# 🚗 Deteksi Parkiran Otomatis dengan Flask, OpenCV, dan CvZone

Selamat datang di proyek **Deteksi Parkiran Otomatis**, sebuah sistem cerdas berbasis web yang dapat **mendeteksi slot parkir kosong atau terisi secara real-time** menggunakan video rekaman area parkir. Sistem ini cocok digunakan untuk **monitoring parkir di area publik, gedung, atau mall** dengan interface modern dan interaktif.

## ✨ Fitur Unggulan

- ✅ Upload video rekaman parkiran langsung via web
- 🟩 Tandai slot parkir secara interaktif (klik 4 titik di canvas)
- 🧠 Deteksi slot kosong/terisi secara real-time
- 📈 Threshold bisa disesuaikan untuk mengatur sensitivitas deteksi
- 📦 Penyimpanan koordinat area parkir dalam file `.pkl`
- 🔁 Tampilan video looping tanpa reload

## 🖥️ Tampilan Awal Interface

![image](https://github.com/user-attachments/assets/cee4fc9c-f0c9-476c-afbb-1e3690e5c8f6)

> Live video feed akan menampilkan area parkir beserta status setiap slot parkir dalam bentuk kotak berwarna:
> - 🟩 Hijau = Kosong
> - 🟥 Merah = Terisi

## 🚀 Cara Menjalankan Aplikasi

### 1. Clone Repository
```bash
git clone https://github.com/Pitooo01/Parking-Slot-Detection.git
cd Parking-Slot-Detection
```

### 2. Install Dependencies
Pastikan kamu menggunakan Python 3.7+  
```bash
pip install -r requirements.txt
```

### 3. Jalankan Server
```bash
python main.py
```

Buka browser dan akses:  
📍 [http://localhost:8000](http://localhost:8000)

## 📂 Struktur Direktori

```
.
├── static/
│   ├── uploads/          # Tempat penyimpanan video yang diunggah
│   └── coordinate/       # File koordinat parkir disimpan (format .pkl)
├── templates/
│   └── index.html        # Halaman utama
├── main.py               # File utama backend Flask
└── README.md             # Dokumentasi proyek ini
└── requirements.txt      # Library yang perlu di install
```

## ⚠️ Catatan Penting

- Pastikan kamu sudah memiliki `car.png` sebagai favicon di folder `static/`
- Gunakan video parkiran yang kualitasnya cukup jelas agar deteksi akurat
- Saat menandai slot, klik 4 titik membentuk kotak (urutan tidak masalah)

## 🧠 Teknologi yang Digunakan

- **Flask**: Framework web backend Python
- **OpenCV**: Deteksi gambar dan pengolahan video
- **CvZone**: Library tambahan visualisasi OpenCV
- **HTML/CSS + JS (Toastr + jQuery)**: Antarmuka modern & responsif

## 📸 Contoh Hasil Deteksi

![image](https://github.com/user-attachments/assets/2c85db66-ce7e-45d2-bae7-5c87927137fb)

## 🙌 Kontribusi

Proyek ini bersifat open source. Jika kamu ingin menambahkan fitur baru, memperbaiki bug, atau mempercantik tampilan – silakan fork repo ini dan pull request!

## 🧑‍💻 Developer

**ALFITO DWITAMA**  
📫 Email: alfito.dwitama@gmail.com
📷 Instagram: [@alfitodwitamaaa](https://www.instagram.com/alfitodwitamaaa)

---

> “Teknologi bukan hanya soal kecanggihan, tapi bagaimana ia menyelesaikan masalah nyata.” 🚀
