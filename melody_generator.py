import random

note_codes = {
    'A' : 0,
    'A#': 1,
    'B' : 2,
    'C' : 3,
    'C#': 4,
    'D' : 5,
    'D#': 6,
    'E' : 7,
    'F' : 8,
    'F#': 9,
    'G' : 10,
    'G#': 11
    } 
note_names = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
classes = {
    'A'  : 0,
    'Am' : 1,
    'A#' : 2,
    'Am#': 3,
    'B'  : 4,
    'Bm' : 5,
    'C'  : 6,
    'Cm' : 7,
    'C#' : 8,
    'Cm#': 9,
    'D'  : 10,
    'Dm' : 11,
    'D#' : 12,
    'Dm#': 13,
    'E'  : 14,
    'Em' : 15,
    'F'  : 16,
    'Fm' : 17,
    'F#' : 18,
    'Fm#': 19,
    'G'  : 20,
    'Gm' : 21,
    'G#' : 22,
    'Gm#': 23
    }

names = ['A', 'Am', 'A#', 'Am#', 'B', 'Bm', 'C', 'Cm', 'C#', 'Cm#', 'D', 'Dm', \
 'D#', 'Dm#', 'E', 'Em', 'F', 'Fm', 'F#', 'Fm#', 'G', 'Gm', 'G#', 'Gm#']

maj_pentatonic_scale = [0, 2, 4, 7, 9]
min_pentatonic_scale = [0, 3, 5, 7, 10]


scales = [
    [0, 2, 4, 5, 7, 9, 11], #maj
    [0, 2, 3, 5, 7, 8, 10] #min
]

probs = [3, 6, 5, 0.1, 5, 6, 2]

tension_border = 12
tensions = [
    [0, 2, 3, 2, 1, 2, 6],
    [-10, 2, 1, -5, -5, 4, 5],
    [-8, 2, 2, -6, -5, 3, 4],
    [-6, 3, 2, 1, -5, 2, 3],
    [-4, 3, 2, 1, 1, 2, 3],
    [-4, 3, 2, -2, -4, 2, 3],
    [-6, 2, 3, -2, -3, 2, 4],
]

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

        melody = [chord // 4, 4]
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
            semiqs_left -= length
            melody.append((chord // 4 + scales[chord % 2][next_step]) % 12)
            melody.append(length)
        
            prev_step = next_step

        melody.append(chord // 4)
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

            track.append(Message('note_on', note=pitch + 57, velocity=80, time=0))
            print(second2tick(semiq*duration, 960, tempo2bpm(tempo)))
            track.append(Message('note_on', note=pitch + 57, velocity=0, time=int(second2tick(semiq*duration, 120, tempo2bpm(tempo)))))
            
        mid.save(name)    
        