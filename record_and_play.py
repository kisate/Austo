import sounddevice as sd

samplerate = 44100
duration = 10

myrecording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)

sd.wait()

sd.play(myrecording)

sd.wait()