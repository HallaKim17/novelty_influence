# Novelty and Influence of Classical Piano Music
***

paper: 

## Installation
To run the code locally, follow the steps below to install required libraries.
1. Install python:
- python >= 3.8.5
3. Other requirements:
- pip install -e .

## Quick Start: Compute Novelty and Influence scores and Draw Figures
- Compute novelty and Influence scores of the piano dataset used in our paper.
```
python main.py
```

- Draw figures of H-novelty, P-novelty, and Influence scores of composers in the dataset used in our paper.
```
PLOT=<one of 'H-novelty', 'P-novelty', 'Influence'>

python figure.py --plot ${PLOT}
```
- `--plot` is REQUIRED argument.
- If you want to specify a list of composers for whom you'd like to draw Influence scores, `--composers` (optional) can be used. For example, to plot the influence scores of Mozart and Beethoven:
```
python figure.py --plot 'Influence' --composers 'Mozart, Beethoven'
```

## Make Custom Dataset: Compute Novelty and Influence Scores of My Own Dataset
1. Make Custom Dataset
- Put your 'mid' files in the `data/midi/custom` directory. Create subfolders specified by the name of each composer and place their respective compositions inside each folder.
- Open `data/meta/custom/metadata_custom.csv` file and fill in the 'composer', 'song_name', 'year', and 'era' (optional) of each song you put in `data/midi/custom` directory. Note that the string of 'composer'  and 'song_name' MUST MATCH the name of a subfolder and a midi file, respectively.
  
  ```
  +-- data
      +-- meta
          +-- custom
              +-- metadata_custom.csv --> edit this file
          +-- novinf
      +-- midi
          +-- custom
              +-- Liszt
              +-- Debussy
              +-- Create a subfolder with a composer name
          +-- novinf
      +-- preprocessed
          +-- custom
          +-- novinf
  ```

- After adding your midi files and finish editing `metadata_custom.csv` file, run the code below to preprocess the midi files.
  ```
  python dataset.py
  ```
2. Compute Novelty and Influence scores
```
python main.py --custom_dataset True
```

3. Plot Figures
```
PLOT=<one of 'H-novelty', 'P-novelty', 'Influence'>

python figure.py --plot ${PLOT} --custom_dataset True
```
You can also specify a list of composers to plot Influence scores as mentioned above.





