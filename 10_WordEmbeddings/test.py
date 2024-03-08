import requests
from tqdm import tqdm
import json

from spacy.lang.de.stop_words import STOP_WORDS
import treetaggerwrapper

import de_dep_news_trf

from icecream import ic

nlp = de_dep_news_trf.load()

file_write = open(r"C:\Users\vruser01\OneDrive - P.ARC AG\affairs.json", "w", encoding="utf-8")
file_read = open(r"C:\Users\vruser01\OneDrive - P.ARC AG\affairs.json", "r", encoding="utf-8")


def get_data(url):
    r = requests.get(url, headers={"Accept": "application/json", "charset": "utf-8"})
    try:
        return r.json()
    except:
        return None


def clean_text(text_raw):
    text = ''
    doc = nlp(text_raw)
    clean = [token for token in doc if not
             token.is_punct and not token.is_digit and not token.is_currency
             and not token.is_bracket and len(token.text) > 1]
    for token in clean:
        text += token.text.lower().replace(';</p><p>-', ' ').replace('</p>', ' ').replace('<p>', ' ').replace('</p', ' ').replace('/p><p', ' ') + " "
    return text


def tag_text(cleaned_text):
    tagger = treetaggerwrapper.TreeTagger(
        TAGLANG='de',
        TAGPARFILE=r"C:\TreeTagger\lib\german.par",
        TAGABBREV=r"C:\TreeTagger\lib\german-abbreviations"
    )
    tags = treetaggerwrapper.make_tags(tagger.tag_text(cleaned_text))
    out_dict = {"Words": [], "Tags": [], "Lemmas": []}
    for idx, tag in enumerate(tags):
        lemma = tag[2]
        if len(lemma) == 1:
            continue
        elif "+" in lemma or "@" in lemma:
            out_dict["Words"].append(tag[0])
            out_dict["Tags"].append(tag[1])
            out_dict["Lemmas"].append(tag[0])
        else:
            out_dict["Words"].append(tag[0])
            out_dict["Tags"].append(tag[1])
            out_dict["Lemmas"].append(tag[-1])

    return out_dict


def download():
    lst_details = []

    for i in tqdm(range(1, 1183), total=1184, desc="Downloading", leave=False):
        for affair in get_data(url=f"https://ws-old.parlament.ch/affairs?pageNumber={i}&lang=de"
                                   f"&format=json"):
            details = get_data(url=f'https://ws-old.parlament.ch/affairs/{affair["id"]}?lang=de&format=json')
            if details["affairType"]["id"] in [1, 2, 3, 4, 7, 10]:
                continue
            elif "councillor" in list(details["author"].keys()):
                subbmitted_by = details["author"]["councillor"]["id"]
                person_details = get_data(
                    url=f"https://ws-old.parlament.ch/councillors/{subbmitted_by}?lang=de&format=json")
                if "party" in person_details.keys():
                    party = person_details["party"]
                    details["author"]["councillor"]["party"] = party

            cleaned_text = ""
            for text in details["texts"]:
                if isinstance(text, dict):
                    t = ""
                    if "type" in text.keys():
                        if text["type"]["id"] in [1, 5]:
                            t += " " + text["value"]

                    cleaned_text += " " + clean_text(t)
            tagged_text = tag_text(cleaned_text)
            details["texts"].append({"cleaned": cleaned_text})
            details["texts"].append({"tagged": tagged_text})

            lst_details.append(details)

    json.dump(lst_details, file_write, indent=3, ensure_ascii=False)


download()


def associate_with_party():
    affairs_list = json.load(file_read)
    for idx, affair in tqdm(enumerate(affairs_list), total=len(affairs_list), desc="Associating with party..."):
        if affair["affairType"]["id"] in [1, 2, 3, 4, 7, 10]:
            affairs_list.pop(idx)
        elif "councillor" in list(affair["author"].keys()):
            subbmitted_by = affair["author"]["councillor"]["id"]
            person_details = get_data(
                url=f"https://ws-old.parlament.ch/councillors/{subbmitted_by}?lang=de&format=json")
            if "party" in person_details.keys():
                party = person_details["party"]
                affair["author"]["councillor"]["party"] = party
        else:
            affairs_list.pop(idx)
    json.dump(affairs_list, file_write)


# associate_with_party()

file_write.close()
