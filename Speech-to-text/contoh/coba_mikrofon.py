import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as sumber:
    print("Menyesuaikan dengan suara sekitar... diam sebentar")
    recognizer.adjust_for_ambient_noise(sumber, duration=1)

    while True:
        print("Silahkan bicara... (ucapkan 'selesai' untuk berhenti)")
        try:
            audio = recognizer.listen(sumber, timeout=5, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            print("Tidak ada suara terdeteksi")
            continue

        print("Sedang memproses...")

        try:
            teks = recognizer.recognize_google(audio, language="id-ID")
            print(f"Kamu bilang : {teks}")
        except sr.UnknownValueError:
            print("Suara tidak bisa dikenali.")
            continue
        except sr.RequestError as e:
            print("Gagal terhubung ke layanan Google:", e)
            continue

        if "selesai" in teks.lower():
            print("Selesai merekam.")
            break
