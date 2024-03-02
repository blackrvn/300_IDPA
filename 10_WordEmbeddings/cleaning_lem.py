import glob
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
        ic(nf)
        for idx, lemma in enumerate(df["Lemma"]):
            words = model(str(lemma))
            for token in words:
                if not token.is_punct and not token.is_digit and not token.is_bracket and not token.is_currency and not token.is_quote and not token.is_stop and token.text not in STOP_WORDS:

                    if "+" not in token.text and "@" not in token.text:
                        lemma_file.write(f"{token.text.lower()}\n")

    lemma_file.close()
