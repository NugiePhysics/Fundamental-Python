from faster_whisper import WhisperModel

model = WhisperModel("small", device="cpu", compute_type="int8")

segments, info = model.transcribe("audio/contoh.wav", language="id")

print(f"Bahasa: {info.language}, durasi: {info.duration:.1f} detik")

teks_lengkap = ""
for seg in segments:
    print(f"[{seg.start:.1f}s - {seg.end:.1f}s] {seg.text}")
    teks_lengkap += seg.text

print("\nHasil akhir:", teks_lengkap.strip())