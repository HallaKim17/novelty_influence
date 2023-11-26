
import dill
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
from music21 import converter
from util import get_pitches
import os
import argparse

# music21를 사용한 일반적인 방법으로 미디 파일 열기
def open_midi(midi_path):
    score = converter.parse(midi_path, quantizePost=False)
    return score


def get_codewords(metadata):
    codewords = {i:[] for i in metadata.index}

    dataset_dir = "../data/midi/custom"
    failed = []
    
    for i in tqdm(metadata.index):
        filename = metadata.song_name[i]
        composer = metadata.composer[i]
        filepath = os.path.join(dataset_dir, composer, filename)
        try:
            mid = open_midi(filepath)
            
            chordify = mid.flat.notes.chordify()
            for element in chordify:
                if element.isChord:
                    codewords[i].append(element.pitches)
                
        except:
            print(f'Failed to read midi file: {filepath}')
            failed.append(filepath)
            continue

    return codewords, failed

def load_codewords(song_idx, custom=False):
    if custom:
        dir_path = "../data/preprocessed/custom"
    else:
        dir_path = "../data/preprocessed/novinf"
    with open(os.path.join(dir_path, f'song_{song_idx}.pkl'), "rb") as f:
        x = dill.load(f)
    x = get_pitches(x)
    return x


if __name__ == "__main__":

    custom_metadata_path = '../data/meta/custom/metadata_custom.csv'
    metadata = pd.read_csv(custom_metadata_path, index_col=0)
    metadata = metadata.sort_values(by=['year'], ascending=True)
    
    Codewords, failed = get_codewords(metadata)
    print(f"Failed to read {len(failed)} midi files: ", failed)
    
    for key in tqdm(Codewords):
        with open(f'../data/preprocessed/custom/song_{key}.pkl', "wb") as f:
            dill.dump(Codewords[key], f)
    print("--- Finished Loading and Preprocessing Custom Dataset ---")




