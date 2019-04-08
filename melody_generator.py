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
probs = [2, 3, 1, 3, 2]

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
        total = sum(probs)
        chosen = random.uniform(0, total)
        cumulative = 0

        for i, x in enumerate(probs):
            cumulative += x
            if cumulative > chosen:
                return (i + current - 2) % 5



    def generate(self, chord_seq, beats_per_chord=8):

        seq_len = len(chord_seq)

        matches = [list(set(self.chords[names[chord_seq[i]]]) & set(self.chords[names[chord_seq[(i+1) % seq_len]]])) for i in range(seq_len)]
    
        melody = []

        for i, chord in enumerate(chord_seq):
            time = [chord // 2] * beats_per_chord
            if len(matches[i]) > 0:
                time[beats_per_chord-1] = matches[i][random.randint(0, len(matches[i]) - 1)]
            if chord % 2 == 0:
                prev_step = random.randint(0, 4)
                time[0] = (time[0] + maj_pentatonic_scale[prev_step]) % 12
                for j in range(1, beats_per_chord):
                    prev_step = self.get_next(prev_step)
                    time[j] = (time[j] + maj_pentatonic_scale[prev_step]) % 12
            else :
                prev_step = random.randint(0, 4)
                time[0] = (time[0] + min_pentatonic_scale[prev_step]) % 12
                for j in range(1, beats_per_chord):
                    prev_step = self.get_next(prev_step)
                    time[j] = (time[j] + min_pentatonic_scale[prev_step]) % 12
            melody.extend(time)
                
    
        return melody

    def write_midi(self, melody, name = 'melody.mid'):
        from midiutil import MIDIFile

        track    = 0
        channel  = 0
        time     = 4    # In beats
        duration = 0.25    # In beats
        tempo    = 50   # In BPM
        volume   = 100  # 0-127, as per the MIDI standard

        MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                            # automatically)
        MyMIDI.addTempo(track, time, tempo)

        for i, pitch in enumerate(melody):
            MyMIDI.addNote(track, channel, pitch + 57, time + i*duration, duration, volume)

        with open(name, "wb") as output_file:
            MyMIDI.writeFile(output_file)
