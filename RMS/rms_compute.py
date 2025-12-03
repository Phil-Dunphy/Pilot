import random
from pydub import AudioSegment

# Zufällige Länge und Sequenz generieren
laenge = random.randint(4, 17)
value = []
print(f"Länge: {laenge}")
for i in range(0, laenge):
    value.append(random.randint(1, 9))
print(f"Sequenz: {value}")

# MP3-Dateien laden
audio_files = {
    1: AudioSegment.from_mp3("data/1.mp3"),
    2: AudioSegment.from_mp3("data/2.mp3"),
    3: AudioSegment.from_mp3("data/3.mp3"),
    4: AudioSegment.from_mp3("data/4.mp3"),
    5: AudioSegment.from_mp3("data/5.mp3"),
    6: AudioSegment.from_mp3("data/6.mp3"),
    7: AudioSegment.from_mp3("data/7.mp3"),
    8: AudioSegment.from_mp3("data/8.mp3"),
    9: AudioSegment.from_mp3("data/9.mp3"),
}

# Leeres Audio-Segment erstellen
combined = AudioSegment.empty()

# Nach der Sequenz zusammenfügen
for num in value:
    combined += audio_files[num]

# Ausgabedatei speichern
combined.export("data/output.mp3", format="mp3")
print("Neue MP3-Datei 'output.mp3' wurde erstellt!")