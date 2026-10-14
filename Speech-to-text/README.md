# Speech-to-Text

Aplikasi pengubah suara menjadi teks (bahasa Indonesia) dengan antarmuka Tkinter. Bisa merekam langsung dari mikrofon atau membaca file audio, memakai salah satu dari dua mesin:

- **Google** (online) — lewat library `SpeechRecognition`, mendukung WAV, FLAC, dan AIFF
- **Whisper** (offline) — lewat `faster-whisper` model `small`, mendukung juga MP3, M4A, dan OGG

## Struktur Proyek

```
Speech-to-text/
├── app.py                # Aplikasi GUI utama
├── contoh/
│   ├── coba_file.py      # Transkripsi file audio dengan Google
│   ├── coba_mikrofon.py  # Transkripsi mikrofon dengan Google (ucapkan "selesai" untuk berhenti)
│   └── coba_whisper.py   # Transkripsi file audio dengan Whisper
├── audio/
│   └── contoh.wav        # Contoh file audio
├── hasil/                # Tempat transkrip yang disimpan (tidak masuk git)
├── requirements.txt
└── README.md
```

## Persyaratan

- Python 3.8 atau lebih baru
- PortAudio untuk `PyAudio` (Debian/Ubuntu: `sudo apt install portaudio19-dev`)
- Tkinter (Debian/Ubuntu: `sudo apt install python3-tk`)
- Koneksi internet untuk mesin Google dan untuk mengunduh model Whisper pertama kali

## Instalasi

```bash
cd Speech-to-text
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Cara Menjalankan

Jalankan semua perintah dari dalam folder `Speech-to-text`, karena path audio dan folder hasil bersifat relatif.

```bash
python app.py                     # aplikasi GUI
python contoh/coba_file.py        # contoh: file audio + Google
python contoh/coba_mikrofon.py    # contoh: mikrofon + Google
python contoh/coba_whisper.py     # contoh: file audio + Whisper
```

Di aplikasi GUI, pilih mesin, lalu klik **Rekam** atau **Pilih File**. Hasil bisa disimpan sebagai `.txt` dengan tombol **Simpan**.
