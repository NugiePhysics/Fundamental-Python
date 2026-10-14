import tkinter as tk
from tkinter import messagebox

import requests

from cuaca_cli import cari_kota, ambil_cuaca, format_laporan

def cek_cuaca(event=None):
    nama = input_kota.get().strip()
    if not nama:
        messagebox.showwarning("Peringatan", "Masukkan nama kota dulu.")
        return

    label_hasil.config(text="Mengambil data...")
    jendela.update_idletasks()   # tampilkan teks loading sebelum menunggu

    try:
        kota = cari_kota(nama)
        if kota is None:
            label_hasil.config(text="")
            messagebox.showerror("Tidak ditemukan", f"Kota '{nama}' tidak ditemukan.")
            return
        cuaca = ambil_cuaca(kota["lat"], kota["lon"])
        label_hasil.config(text=format_laporan(kota, cuaca))
    except requests.exceptions.RequestException:
        label_hasil.config(text="")
        messagebox.showerror("Error", "Gagal mengambil data. Periksa koneksi internet.")

# --- Membangun jendela ---
jendela = tk.Tk()
jendela.title("Aplikasi Cuaca")
jendela.geometry("400x320")
jendela.resizable(False, False)

judul = tk.Label(jendela, text="Aplikasi Cuaca", font=("Arial", 16, "bold"))
judul.pack(pady=10)

input_kota = tk.Entry(jendela, font=("Arial", 12), width=25)
input_kota.pack(pady=5)
input_kota.focus()
input_kota.bind("<Return>", cek_cuaca)   # tekan Enter = klik tombol

tombol = tk.Button(jendela, text="Cek Cuaca", font=("Arial", 11), command=cek_cuaca)
tombol.pack(pady=5)

label_hasil = tk.Label(jendela, text="", font=("Courier", 10), justify="left")
label_hasil.pack(pady=10)

jendela.mainloop()