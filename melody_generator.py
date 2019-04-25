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

probs = [6, 5, 0.1, 5, 6]

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

    def get_next(self, current, tension) : 
        cur_probs = probs.copy()
        cur_tensions = tensions[current]

        for i in range(len(cur_probs)):
            if tension < tension_border:
                if cur_tensions[(current + i - 3) % 7] < 0:
                    cur_probs[i] *= 0.2*tension
                else:
                    cur_probs[i] *= 1.2*(max(1, tension_border + 1 - tension - cur_tensions[i]*0.2))
            else :
                if cur_tensions[(current + i - 3) % 7] < 0:
                    cur_probs[i] *= 1.02*tension
                else:
                    cur_probs[i] *= 0.1
        


        total = sum(cur_probs)
        chosen = random.uniform(0, total)
        cumulative = 0

        for i, x in enumerate(cur_probs):
            cumulative += x
            if cumulative > chosen:
                return (i + current - 3) % 7



    def process_chord(self, chord, beats_per_chord=16):

        melody = [chord // 2, 4]
        tension = 0
        semiqs_left = (beats_per_chord - 2)*4
        prev_step = 0

        while semiqs_left > 0:
            next_step = self.get_next(prev_step, tension)
            
            while (scales[chord % 2][next_step] + chord // 2 in [4, 6]) :
                next_step = self.get_next(prev_step, tension)

            # print(prev_step, next_step)
            tension += tensions[prev_step][next_step]
            tension = max(0, tension)
            if next_step == 0:
                tension = 0
            
            length = random.randint(2, min(4, max(2, tension_border - tension)))
            length = min(length, semiqs_left)
            if (semiqs_left % 16 > 0 and length > semiqs_left % 16):
                length = semiqs_left % 16
                print(semiqs_left)
            semiqs_left -= length
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

        for i in range(len(melody)//2):
            pitch, duration = melody[2*i], melody[1+2*i]

            track.append(Message('note_on', note=pitch + 54, velocity=80, time=0))
        
            track.append(Message('note_on', note=pitch + 54, velocity=0, time=int(second2tick(semiq*duration, 120, tempo2bpm(tempo)))))
            
        mid.save(name)    
        