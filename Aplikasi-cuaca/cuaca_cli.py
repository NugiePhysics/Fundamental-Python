import requests

URL_GEOCODING = "https://geocoding-api.open-meteo.com/v1/search"
URL_CUACA = "https://api.open-meteo.com/v1/forecast"
TIMEOUT = 10

KODE_CUACA = {
    0: "Cerah",
    1: "Cerah berawan",
    2: "Berawan sebagian",
    3: "Mendung",
    45: "Berkabut",
    48: "Kabut beku",
    51: "Gerimis ringan",
    53: "Gerimis",
    55: "Gerimis lebat",
    56: "Gerimis beku ringan",
    57: "Gerimis beku lebat",
    61: "Hujan ringan",
    63: "Hujan sedang",
    65: "Hujan lebat",
    66: "Hujan beku ringan",
    67: "Hujan beku lebat",
    71: "Salju ringan",
    73: "Salju",
    75: "Salju lebat",
    77: "Butiran salju",
    80: "Hujan lokal ringan",
    81: "Hujan lokal sedang",
    82: "Hujan lokal deras",
    85: "Salju lokal ringan",
    86: "Salju lokal lebat",
    95: "Badai petir",
    96: "Badai petir disertai es",
    99: "Badai petir disertai es lebat",
}


def cari_kota(nama_kota):
    parameter = {"name": nama_kota, "count": 1, "language": "id"}
    respon = requests.get(URL_GEOCODING, params=parameter, timeout=TIMEOUT)
    respon.raise_for_status()

    hasil = respon.json().get("results")  # None jika kota tidak ditemukan
    if not hasil:
        return None

    kota = hasil[0]
    return {
        "nama": kota["name"],
        "negara": kota.get("country", ""),
        "lat": kota["latitude"],
        "lon": kota["longitude"],
    }


def ambil_cuaca(lat, lon):
    parameter = {
        "latitude": lat,
        "longitude": lon,
        "current": (
            "temperature_2m,apparent_temperature,relative_humidity_2m,"
            "wind_speed_10m,weather_code"
        ),
        "timezone": "auto",
    }
    respon = requests.get(URL_CUACA, params=parameter, timeout=TIMEOUT)
    respon.raise_for_status()
    return respon.json()["current"]


def deskripsi_cuaca(kode):
    return KODE_CUACA.get(kode, f"Tidak diketahui (kode {kode})")


def format_laporan(kota, cuaca):
    return (
        f"Cuaca di {kota['nama']}, {kota['negara']}\n"
        f"{'-' * 35}\n"
        f"Kondisi       : {deskripsi_cuaca(cuaca['weather_code'])}\n"
        f"Suhu          : {cuaca['temperature_2m']} °C\n"
        f"Terasa seperti: {cuaca['apparent_temperature']} °C\n"
        f"Kelembapan    : {cuaca['relative_humidity_2m']} %\n"
        f"Angin         : {cuaca['wind_speed_10m']} km/jam\n"
        f"Waktu data    : {cuaca['time']}"
    )


def main():
    print("=== Aplikasi Cuaca ===")
    print("Ketik nama kota, atau 'keluar' untuk berhenti")

    while True:
        nama = input("\nNama kota: ").strip()
        if nama.lower() == "keluar":
            print("Sampai jumpa!")
            break
        if not nama:
            print("Nama kota tidak boleh kosong.")
            continue

        try:
            kota = cari_kota(nama)
            if kota is None:
                print(f"Kota '{nama}' tidak ditemukan. Cek ejaannya.")
                continue
            cuaca = ambil_cuaca(kota["lat"], kota["lon"])
        except requests.exceptions.Timeout:
            print("Server terlalu lama merespons. Coba lagi.")
        except requests.exceptions.ConnectionError:
            print("Tidak bisa terhubung. Periksa koneksi internet.")
        except requests.exceptions.RequestException as e:
            print(f"Terjadi kesalahan saat mengambil data: {e}")
        else:
            print()
            print(format_laporan(kota, cuaca))


if __name__ == "__main__":
    main()
