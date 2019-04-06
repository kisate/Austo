

names = ['A', 'Am', 'A#', 'Am#', 'B', 'Bm', 'C', 'Cm', 'C#', 'Cm#', 'D', 'Dm', \
 'D#', 'Dm#', 'E', 'Em', 'F', 'Fm', 'F#', 'Fm#', 'G', 'Gm', 'G#', 'Gm#']


scales = {}

def init_scales():
    for i, name in enumerate(names):
        scale = [0]*24
        scale[i] = 10
        scale[(i+10) % 24] = 4
        scale[(i+14) % 24] = 5
        scales[name] = scale

init_scales()


