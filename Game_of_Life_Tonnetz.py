from collections import Counter
from music21 import *
import sys 

'''John Conway's Game of Life
   Python code for printing generations modified from
   http://rosettacode.org/wiki/Conway%27s_Game_of_Life#Boardless_approach

   Each cell is mapped to a pitch on a Tonnetz
   Each generation is printed, and a midi file is played'''

harmonies = []
myStream = stream.Stream()
melodyStream = stream.Stream()
 
def life(world, N):
    "Play Conway's game of life for N generations from initial world."
    for g in range(N+1):
        display(world, g)
        counts = Counter(n for c in world for n in offset(neighboring_cells, c))
        world = {c for c in counts 
                if counts[c] == 3 or (counts[c] == 2 and c in world)}
        if g==N:
            print("the last generation...")
    musicLife(N+1)

    
def musicLife(x):
    for harmony in harmonies:
        myStream.append(chord.Chord(harmony))
    s = stream.Score(id='Musical Life')
    p1 = stream.Part(id='Melody')
    p2 = stream.Part(id='Chords')
    p1.append(melodyStream)
    p1.insert(instrument.Soprano()) #melody instrument
    p2.append(myStream)
    p2.insert(instrument.Vocalist()) #chord instrument
    # s.insert(0, p1) #uncomment if melody wanted
    s.insert(0, p2) #uncomment if chords wanted
    s.write('midi', '/home/daniel/Desktop/ConwayBunnies') #if uncommented, this will save midi file to path
    s.show('midi')  # this will play a midi file in default midi player
##    s.show() #this brings up a score but gets really messy with the fast notes and complex beat ratios


def musicGame(world):
    midiNotes = []
    chordNotes = []
    melody = []
    for (x, y) in world: #converts the coordinates to a Tonnetz (0, 0) is midi-60
        n = (x*3 + y*4 + 60)  #continuous space
        n2 = ((x*3%12)+(y*4%12)+60)  #modular space
        n3 = (x*5 + y*7 +60) #fifth-based space
        n4 = (x*7 + y*4 + 60) #rotation of n
        midiNotes.append(n4)
        melody.append(note.Note(n4))
        chordNotes.append(note.Note(n4))
    #print(midiNotes)
    for i in chordNotes: #this makes each generation last for a whole note
        i.quarterLength = 4.0
    harmonies.append(chordNotes)
    for i in melody:
        i.quarterLength = 4.0/float(len(melody)) #even note length to fit all in whole note
        melodyStream.append(i)
 
neighboring_cells = [(-1, -1), (-1, 0), (-1, 1), 
                     ( 0, -1),          ( 0, 1), 
                     ( 1, -1), ( 1, 0), ( 1, 1)]


def offset(cells, delta):
    "Slide/offset all the cells by delta, a (dx, dy) vector."
    (dx, dy) = delta
    return {(x+dx, y+dy) for (x, y) in cells}

 
def display(world, g):
    "Display the world as a grid of characters."
    print('          GENERATION {}:'.format(g))

    if len(world) == 0: #if the cells die out before the last generation (prevents error)
        print("all dead")
        musicLife(g)
        sys.exit()

    musicGame(world)

    Xs, Ys = zip(*world)
##    Xrange = range(min(Xs), max(Xs)+1)
##    for y in range(min(Ys), max(Ys)+1):
    Xrange = range(-10, 15)
    for y in range(-10, 15):
    
        print(''.join('#' if (x, y) in world else '.'
                      for x in Xrange))


"""a few sample starting points"""
R_pentomino = {(1, 2), (2, 1), (2, 2), (2, 3), (3, 3)}
figure8 = {(1, 5), (1, 6), (2, 3), (2, 5), (2, 6), (3, 2), (4, 5), (6, 1), (6, 2), (7, 1), (7, 2)}
bunnies = {(1, 0), (0, 3), (2, 1), (2, 2), (3, 0), (5, 1), (6, 2), (6, 3), (7, 1)} #starts small but reproduces quickly
random = {(2, 3), (1, 2), (2, 5), (6, 4), (5, 4), (2, 1), (1, 3), (4, 3)} #only 8 generations
random2 = {(5, 5), (4, 4), (3, 3), (2, 2), (1, 1), (0, 0)} #only 2 generations
random3 = {(0, 0), (1, 1), (0, 1), (4, 4), (5, 5), (4, 5)}
blinker = {(1, 0), (1, 1), (1, 2)}#blinks back and forth every generation
block   = {(0, 0), (1, 1), (0, 1), (1, 0)} #static (and dissonant)
toad    = {(1, 2), (0, 1), (0, 0), (0, 2), (1, 3), (1, 1)}
glider  = {(0, 1), (1, 0), (0, 0), (0, 2), (2, 1)} #lower, and lower, and lower...
GosperGliderGun = {(1, 4), (1, 5), (2, 4), (2, 5), (11, 3), (11, 4), (11, 5), (12, 2), (12, 6), (13, 1), (13, 7), (14, 1), (14, 7), (15, 4), (16, 2), (16, 6), (17, 3), (17, 4), (17, 5), (18, 4), (21, 5), (21, 6), (21, 7), (22, 5), (22, 6), (22, 7), (23, 4), (23, 8), (25, 3), (25, 4), (25, 8), (25, 9), (35, 6), (35, 7), (36, 6), (36, 7)}
world   = (block | offset(blinker, (5, 2)) | offset(glider, (15, 5)) | offset(toad, (25, 5))
           | {(18, 2), (19, 2), (20, 2), (21, 2)} | offset(block, (35, 7)))

life(bunnies, 50) #pick a  starting point and a number of generations

