# Aplikasi Cuaca

Aplikasi cuaca sederhana berbahasa Indonesia yang menampilkan kondisi cuaca saat ini untuk kota mana pun. Tersedia dalam dua versi: **CLI** (terminal) dan **GUI** (Tkinter). Data diambil dari [Open-Meteo](https://open-meteo.com/), tanpa API key.

## Fitur

- Pencarian kota berdasarkan nama (geocoding Open-Meteo)
- Menampilkan kondisi, suhu, suhu terasa, kelembapan, kecepatan angin, dan waktu data
- Deskripsi cuaca dalam bahasa Indonesia (berdasarkan kode cuaca WMO)
- Penanganan error: kota tidak ditemukan, tidak ada koneksi, dan timeout
- Satu logika bersama: versi GUI memakai fungsi dari versi CLI

## Struktur Proyek

```
Aplikasi-cuaca/
├── cuaca_cli.py       # Versi terminal + fungsi inti (cari_kota, ambil_cuaca, format_laporan)
├── cuaca_gui.py       # Versi GUI (Tkinter), memakai fungsi dari cuaca_cli.py
├── contoh/
│   └── coba_api.py    # Percobaan awal memanggil API Open-Meteo
├── requirements.txt
└── README.md
```

## Persyaratan

- Python 3.8 atau lebih baru
- Library [`requests`](https://pypi.org/project/requests/)
- Tkinter (hanya untuk versi GUI; biasanya sudah termasuk di Python. Di Debian/Ubuntu: `sudo apt install python3-tk`)

## Instalasi

```bash
git clone <url-repositori>
cd Aplikasi-cuaca

python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Cara Menjalankan

### Versi CLI

```bash
python cuaca_cli.py
```

Contoh sesi:

```
=== Aplikasi Cuaca ===
Ketik nama kota, atau 'keluar' untuk berhenti

Nama kota: Pontianak

Cuaca di Kota Pontianak, Indonesia
-----------------------------------
Kondisi       : Cerah
Suhu          : 31.5 °C
Terasa seperti: 39.4 °C
Kelembapan    : 69 %
Angin         : 6.7 km/jam
Waktu data    : 2026-10-14T12:15

Nama kota: keluar
Sampai jumpa!
```

### Versi GUI

```bash
python cuaca_gui.py
```

Ketik nama kota, lalu tekan **Enter** atau klik **Cek Cuaca**.

## Cara Kerja

1. `cari_kota(nama)` memanggil Geocoding API untuk mendapatkan nama resmi, negara, lintang, dan bujur.
2. `ambil_cuaca(lat, lon)` memanggil Forecast API untuk mengambil data cuaca saat ini.
3. `format_laporan(kota, cuaca)` menyusun hasilnya menjadi teks yang siap ditampilkan.

## API yang Digunakan

| Fungsi | Endpoint |
| --- | --- |
| Geocoding | `https://geocoding-api.open-meteo.com/v1/search` |
| Cuaca saat ini | `https://api.open-meteo.com/v1/forecast` |

Open-Meteo gratis untuk penggunaan non-komersial. Lihat [syarat penggunaannya](https://open-meteo.com/en/terms).

## Lisensi

Belum ditentukan. Tambahkan file `LICENSE` sebelum dipublikasikan jika ingin proyek ini dipakai orang lain.
