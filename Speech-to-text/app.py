import io
import os
import threading
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, scrolledtext

import speech_recognition as sr

FORMAT_GOOGLE = (".wav", ".flac", ".aiff", ".aif")


class AplikasiSTT:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech-to-Text")
        self.root.geometry("640x480")

        self.recognizer = sr.Recognizer()
        self.model_whisper = None  # dimuat hanya saat pertama dibutuhkan
        self.mesin = tk.StringVar(value="google")

        self.buat_tampilan()

    # ---------- Bagian tampilan ----------
    def buat_tampilan(self):
        # Pilihan mesin
        frame_mesin = tk.Frame(self.root)
        frame_mesin.pack(pady=8)
        tk.Label(frame_mesin, text="Mesin:").pack(side=tk.LEFT)
        tk.Radiobutton(frame_mesin, text="Google (online)",
                       variable=self.mesin, value="google").pack(side=tk.LEFT)
        tk.Radiobutton(frame_mesin, text="Whisper (offline)",
                       variable=self.mesin, value="whisper").pack(side=tk.LEFT)

        # Tombol-tombol
        frame_tombol = tk.Frame(self.root)
        frame_tombol.pack(pady=4)
        self.btn_rekam = tk.Button(frame_tombol, text="Rekam", width=12,
                                   command=self.klik_rekam)
        self.btn_file = tk.Button(frame_tombol, text="Pilih File", width=12,
                                  command=self.klik_pilih_file)
        self.btn_rekam.pack(side=tk.LEFT, padx=4)
        self.btn_file.pack(side=tk.LEFT, padx=4)
        tk.Button(frame_tombol, text="Simpan", width=12,
                  command=self.simpan).pack(side=tk.LEFT, padx=4)
        tk.Button(frame_tombol, text="Hapus", width=12,
                  command=self.hapus).pack(side=tk.LEFT, padx=4)

        # Kotak hasil
        self.kotak_teks = scrolledtext.ScrolledText(self.root, wrap=tk.WORD,
                                                    font=("Arial", 11))
        self.kotak_teks.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        # Baris status
        self.label_status = tk.Label(self.root, text="Siap", anchor="w",
                                     relief=tk.SUNKEN)
        self.label_status.pack(fill=tk.X, side=tk.BOTTOM)

    def set_status(self, pesan):
        # Aman dipanggil dari thread mana pun
        self.root.after(0, lambda: self.label_status.config(text=pesan))

    def atur_tombol(self, aktif):
        keadaan = tk.NORMAL if aktif else tk.DISABLED
        self.btn_rekam.config(state=keadaan)
        self.btn_file.config(state=keadaan)

    # ---------- Menjalankan pekerjaan di latar belakang ----------
    def jalankan_di_latar(self, fungsi, *args):
        self.atur_tombol(False)

        def tugas():
            try:
                teks = fungsi(*args)
                self.root.after(0, self.tampilkan_hasil, teks)
            except Exception as e:
                self.root.after(0, messagebox.showerror, "Terjadi kesalahan", str(e))
            finally:
                self.root.after(0, self.atur_tombol, True)
                self.set_status("Siap")

        threading.Thread(target=tugas, daemon=True).start()

    # ---------- Aksi tombol ----------
    def klik_rekam(self):
        self.jalankan_di_latar(self.rekam_mikrofon)

    def klik_pilih_file(self):
        path = filedialog.askopenfilename(
            title="Pilih file audio",
            filetypes=[("File audio", "*.wav *.flac *.aiff *.mp3 *.m4a *.ogg"),
                       ("Semua file", "*.*")])
        if not path:
            return
        if self.mesin.get() == "google" and not path.lower().endswith(FORMAT_GOOGLE):
            messagebox.showwarning(
                "Format tidak didukung",
                "Mesin Google hanya bisa membaca WAV, FLAC, atau AIFF.\n"
                "Pilih mesin Whisper untuk MP3/M4A.")
            return
        self.jalankan_di_latar(self.proses_file, path)

    def simpan(self):
        isi = self.kotak_teks.get("1.0", tk.END).strip()
        if not isi:
            messagebox.showinfo("Kosong", "Belum ada teks untuk disimpan.")
            return
        os.makedirs("hasil", exist_ok=True)
        nama_default = datetime.now().strftime("transkrip_%Y%m%d_%H%M%S.txt")
        path = filedialog.asksaveasfilename(
            initialdir="hasil", initialfile=nama_default,
            defaultextension=".txt", filetypes=[("File teks", "*.txt")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(isi)
            self.set_status(f"Tersimpan: {os.path.basename(path)}")

    def hapus(self):
        self.kotak_teks.delete("1.0", tk.END)

    def tampilkan_hasil(self, teks):
        jam = datetime.now().strftime("%H:%M:%S")
        self.kotak_teks.insert(tk.END, f"[{jam}] {teks}\n\n")
        self.kotak_teks.see(tk.END)

    # ---------- Logika speech-to-text ----------
    def rekam_mikrofon(self):
        with sr.Microphone() as sumber:
            self.set_status("Menyesuaikan dengan suara sekitar...")
            self.recognizer.adjust_for_ambient_noise(sumber, duration=1)
            self.set_status("Silakan bicara...")
            try:
                audio = self.recognizer.listen(sumber, timeout=5,
                                               phrase_time_limit=30)
            except sr.WaitTimeoutError:
                raise Exception("Tidak ada suara terdeteksi.")
        self.set_status("Memproses suara...")
        return self.ubah_jadi_teks(audio=audio)

    def proses_file(self, path):
        self.set_status(f"Memproses {os.path.basename(path)}...")
        return self.ubah_jadi_teks(path=path)

    def muat_whisper(self):
        if self.model_whisper is None:
            self.set_status("Memuat model Whisper (pertama kali agak lama)...")
            from faster_whisper import WhisperModel
            self.model_whisper = WhisperModel("small", device="cpu",
                                              compute_type="int8")
        return self.model_whisper

    def ubah_jadi_teks(self, audio=None, path=None):
        if self.mesin.get() == "google":
            if audio is None:
                with sr.AudioFile(path) as sumber:
                    audio = self.recognizer.record(sumber)
            try:
                return self.recognizer.recognize_google(audio, language="id-ID")
            except sr.UnknownValueError:
                raise Exception("Suara tidak bisa dikenali.")
            except sr.RequestError:
                raise Exception("Tidak bisa terhubung ke Google. "
                                "Cek internet atau pakai mesin Whisper.")
        else:
            model = self.muat_whisper()
            self.set_status("Whisper sedang mentranskripsi...")
            sumber = path if path else io.BytesIO(audio.get_wav_data())
            segments, _ = model.transcribe(sumber, language="id")
            teks = "".join(seg.text for seg in segments).strip()
            if not teks:
                raise Exception("Tidak ada ucapan yang terdeteksi.")
            return teks


if __name__ == "__main__":
    root = tk.Tk()
    AplikasiSTT(root)
    root.mainloop()