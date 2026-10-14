# Belajar Python

Kumpulan materi belajar dan proyek kecil Python.

## Isi Repositori

| Folder | Isi |
| --- | --- |
| [Python-Fundamental](Python-Fundamental/) | Notebook dasar Python: variabel, string, angka, kondisi, fungsi, perulangan, dictionary & set, modul, dan error handling |
| [Python-Library](Python-Library/) | Notebook pengenalan library (NumPy) |
| [Aplikasi-cuaca](Aplikasi-cuaca/) | Aplikasi cuaca CLI dan GUI memakai API Open-Meteo |
| [Speech-to-text](Speech-to-text/) | Aplikasi GUI pengubah suara menjadi teks (Google / Whisper) |

Setiap proyek aplikasi punya `README.md` dan `requirements.txt` sendiri.

## Menjalankan Notebook

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Lalu buka file `.ipynb` di VS Code atau Jupyter dan pilih kernel dari `.venv`.
