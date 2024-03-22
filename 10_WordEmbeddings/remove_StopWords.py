import json
from spacy.lang.de.stop_words import STOP_WORDS
from tqdm import tqdm

from icecream import ic

read_file = open(r"C:\Users\lukas\Downloads\affairs.json", 'r', encoding='utf-8')
write_file = open(r"C:\Users\lukas\Downloads\test.json", 'w', encoding='utf-8')
read_json = json.load(read_file)

new_json = read_json

for affair in tqdm(new_json, total=len(new_json)):
    texts = affair['texts']
    for text in texts:
        if "tagged" in text.keys():
            word = text["tagged"]["Words"]
            lemmas = text["tagged"]["Lemmas"]
            tags = text["tagged"]["Tags"]
            for idx, lemma in enumerate(lemmas):
                if lemma not in STOP_WORDS and lemma != 'die' and len(lemma) > 1:
                    pass
                else:
                    word.pop(idx)
                    lemmas.pop(idx)
                    tags.pop(idx)

            while lemmas.count('die'):
                i = lemmas.index('die')
                lemmas.remove('die')
                word.pop(i)
                tags.pop(i)


json.dump(new_json, write_file, ensure_ascii=False, indent=3)