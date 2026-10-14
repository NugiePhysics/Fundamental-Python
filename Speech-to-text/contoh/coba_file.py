import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.AudioFile("audio/contoh.wav") as sumber:
    audio = recognizer.record(sumber)

try:
    teks = recognizer.recognize_google(audio, language="id-ID")
    print(f"Hasil : {teks}")
except sr.UnknownValueError:
    print("Suara tidak bisa dikenali")
except sr.RequestError as e:
    print("Gagal terhubung ke layanan Google:", e)