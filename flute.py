import sounddevice as sd

duration = 15
fs = 44100

myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)

sd.wait()

print(myrecording)

sd.play(myrecording)

sd.wait()