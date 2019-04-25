from mido import MidiFile

mid = MidiFile('midi/ode.mid')

for msg in mid:
    print(int(1000*msg.time))