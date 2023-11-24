from tqdm import tqdm
import dill
import os
import argparse
import pandas as pd
from util import get_pitches
from novelty import compute_H_novelty, compute_P_novelty
from influence import compute_influence


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--custom_dataset', type=bool, default=False)
    
    args = parser.parse_args()

    if args.custom_dataset:
        metadata_path = '../data/meta/custom/metadata_custom.csv'
        data_path = '../data/preprocessed/custom/'
        result_path = 'result/custom/'
    else:
        metadata_path = '../data/meta/novinf/metadata.csv'
        data_path = '../data/preprocessed/novinf/'
        result_path = 'result/novinf'

    metadata = pd.read_csv(metadata_path, index_col=0)

    Codewords = {}
    for idx in tqdm(metadata.index):
        with open(os.path.join(data_path, f'song_{idx}.pkl'), "rb") as f:
            x = dill.load(f)
            Codewords[idx] = x
    Codewords = {k: get_pitches(v) for k,v in Codewords.items()}

    # compute H-novelty
    H_Novelty = compute_H_novelty(df=metadata, 
                                codewords=Codewords,
                                num_unique_cws=2**88) # number of combinations of all piano keys
    with open(os.path.join(result_path,'H-Novelty.pkl'), 'wb') as f:
        dill.dump(H_Novelty, f)

    # compute P-novelty
    P_Novelty = compute_P_novelty(df=metadata, 
                                codewords=Codewords,
                                num_unique_cws=2**88) # number of combinations of all piano keys
    with open(os.path.join(result_path,'P-Novelty.pkl'), 'wb') as f:
        dill.dump(P_Novelty, f)


    # compute influence
    Influence = compute_influence(df=metadata,
                                  codewords=Codewords) 
    with open(os.path.join(result_path,'Influence.pkl'), 'wb') as f:
        dill.dump(Influence, f)

