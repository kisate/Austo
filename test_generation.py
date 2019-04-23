from melody_generator import MelodyGenerator

gen = MelodyGenerator()

melody = gen.generate(6)

print(melody)

gen.write_midi(melody, 'midi/m.mid')