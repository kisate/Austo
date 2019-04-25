import random
from stuff import *

pentatonic_scales = [
    [0, 2, 4, 7, 9], #maj
    [0, 3, 5, 7, 10] #min
]

scales = [
    [0, 2, 4, 5, 7, 9, 11], #maj
    [0, 2, 3, 5, 7, 8, 10] #min
]

probs = [6, 7, 1, 7, 6]
length_probs = [1, 7, 2, 1]
pause_prob = 0

tension_border = 12

class MelodyGenerator():
    
    def init_chords(self, chords):
        for i, name in enumerate(names):

            n = i // 2

            if (i % 2 == 0):
                chords[name] = [n % 12, (n+4) % 12, (n+7) % 12]
            else :
                chords[name] = [n % 12, (n+3) % 12, (n+7) % 12]
    
    def __init__(self):
        self.chords = {}
        self.init_chords(self.chords)      

    def get_next(self, current) :         
        return (self.get_random_index(probs) + current - 2) % 5
        
    def get_random_index(self, probabillities):
        total = sum(probabillities)
        chosen = random.uniform(0, total)
        cumulative = 0

        for i, x in enumerate(probabillities):
            cumulative += x
            if cumulative > chosen:
                return i


    def process_chord(self, chord, beats_per_chord=8):

        melody = [chord // 2, 4]
        length_left = 12
        semiqs_left = (beats_per_chord - 2)*4
        prev_step = 0

        while semiqs_left > 0:
            next_step = self.get_next(prev_step)
            
            while (scales[chord % 2][next_step] + chord // 2 in [4, 6, 9, 11, 1]) :
                next_step = self.get_next(prev_step)

            # print(prev_step, next_step)

            length = self.get_random_index(length_probs) + 1

            length = min(length, semiqs_left, length_left)

            semiqs_left -= length
            length_left -= length

            if (length_left == 0) :
                length_left = 16


            if (random.random() < pause_prob):
                melody.append(12)
            else:
                melody.append((chord // 2 + scales[chord % 2][next_step]) % 12)
            melody.append(length)
            
        
            prev_step = next_step

        melody.append(chord // 2)
        melody.append(4)

        return melody

    def generate(self, sequence):
        melody = []
        for chord in sequence:
            part = self.process_chord(chord)
            melody.extend(part)
            # part = self.process_chord(chord)
            # melody.extend(part)
        return melody

    def write_midi(self, melody, name = 'melody.mid'):
        from mido import Message, MidiFile, MidiTrack, MetaMessage, tempo2bpm, second2tick

        tempo = 120


        mid = MidiFile(ticks_per_beat=120)
        track = MidiTrack()
        mid.tracks.append(track)

        track.append(MetaMessage('set_tempo', tempo = int(tempo2bpm(tempo)), time=0))
        

        

        beat = 60/tempo
        semiq = beat/4
        pause = 0

        for i in range(len(melody)//2):
            pitch, duration = melody[2*i], melody[1+2*i]

            if (pitch < 12):
                track.append(Message('note_on', note=pitch + 66, velocity=80, time=pause))
                pause = 0
                track.append(Message('note_on', note=pitch + 66, velocity=0, time=int(second2tick(semiq*duration, 120, tempo2bpm(tempo)))))
            else :
                pause=int(second2tick(semiq*duration, 120, tempo2bpm(tempo)))

        mid.save(name)    
        