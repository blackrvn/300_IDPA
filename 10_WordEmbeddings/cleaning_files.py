import spacy
from spacy_cleaner import processing, Cleaner
from spacy_cleaner.processing import removers
from icecream import ic

model = spacy.load("de_dep_news_trf")
import de_dep_news_trf
import glob
import os

PATH = r'..\09_Quellen\Parteiprogramme'
clean_path = r'..\09_Quellen\Parteiprogramme\cleaned'

for file in glob.glob(os.path.join(PATH, '*.txt')):
    f_name = file.split('\\')[-1]
    nfile_path = os.path.join(clean_path, f_name)
    print(nfile_path)
    cleaned_file = open(nfile_path, 'w', encoding='utf-8')

    with open(file, 'r', encoding='ANSI') as dirty_file:
        nlp = de_dep_news_trf.load()
        text = dirty_file.read()
        doc = nlp(text)
        no_punct = [token for token in doc if not
        token.is_punct and not token.is_digit and not token.is_currency and not token.is_bracket]
        cleaned_file.write(' '.join(t.text for t in no_punct))
    cleaned_file.close()
