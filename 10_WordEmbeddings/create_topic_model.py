import glob
import os
import spacy
model = spacy.load("de_dep_news_trf")
from spacy.lang.de.stop_words import STOP_WORDS

from icecream import ic

import pandas as pd

path_to_lemma = '..\\09_Quellen\\Parteiprogramme\\tagged\\'

lemmas = {}

for file in glob.glob(path_to_lemma + '*.txt'):
    nf = file.replace(".txt", ".lem")
    lemma_file = open(nf, 'w', encoding="utf-8")
    with open(file, 'r', encoding='utf-8') as f:
        df = pd.read_csv(f, sep='\t', header=None, names=["Wort", "Typ", "Lemma"], dtype={"Lemma": str})
        token_to_drop = []

        for idx, lemma in enumerate(df["Lemma"]):
            words = model(lemma)
            for token in words:
                if token.is_punct or token.is_digit or token.is_bracket or token.is_currency or token.is_quote or token.is_stop or token.text in STOP_WORDS:
                    token_to_drop.append(idx)
                    ic(idx, token)

        cleaned_df = df.drop(idx, axis=0, inplace=False)

        lemmas[file] = cleaned_df["Lemma"]
        ic(cleaned_df)
    lemma_file.write(cleaned_df["Lemma"])

ic(lemmas)
