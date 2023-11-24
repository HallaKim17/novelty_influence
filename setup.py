from setuptools import setup

setup(
    name="novinf",
    packages=["novinf"],
    install_requires=[
        'dill',
        'numpy',
        'pandas',
        'scikit-learn',
        'matplotlib',
        'tqdm',
        'music21==7.3.3'
        'pretty-midi'
    ]
)