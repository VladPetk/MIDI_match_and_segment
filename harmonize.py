from parallelbar import progress_map
import pickle

import argparse
import os
from chorder import Dechorder, Chord
import miditoolkit

def chordify_midi(path_infile): 
    try:
        # load
        midi_obj = miditoolkit.midi.parser.MidiFile(path_infile)
        notes = midi_obj.instruments[0].notes
        notes = sorted(notes, key=lambda x: (x.start, x.pitch))

        # exctract chord
        chords = Dechorder.dechord(midi_obj)
        chord_names = []
        for chord in chords:
            if chord.is_complete():
                chord_info = [chord.root_pc, chord.quality, chord.bass_pc]
                chord_name = [str(x) for x in chord_info]
                chord_names.append([''.join(chord_name), chord_info])
        return chord_names
    except:
        return []

if __name__=='__main__':

    # Define arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--name_in", type=str, help="Specify the name in variable")
    parser.add_argument("--name_out", type=str, help="Specify the name out variable")
    args = parser.parse_args()

    bad_paths = []
    for path, subdirs, files in os.walk("D:/musicai_old/classical_midis/"):
        for name in files:
            bad_paths.append(os.path.join(path, name))

    good_paths = []
    for path, subdirs, files in os.walk("D:/musicai_old/maestro/"):
        for name in files:
            good_paths.append(os.path.join(path, name))

    res = progress_map(chordify_midi, good_paths, process_timeout=50, n_cpu=6)
    pickle.dump(res, open(f"{args.name_out}.p", "wb"))

    res = progress_map(chordify_midi, bad_paths, process_timeout=50, n_cpu=6)
    pickle.dump(res, open(f"{args.name_in}.p", "wb"))

