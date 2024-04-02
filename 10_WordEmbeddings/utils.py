import json
import os
import gensim
from spacy.lang.de.stop_words import STOP_WORDS
import treetaggerwrapper

import de_dep_news_trf

from icecream import ic

nlp = de_dep_news_trf.load()

interested_parties = ["SP", "SVP", "FDP-Liberale", "glp", "GRÜNE", "M-E"]
fractions = {""}

user = os.environ["HOMEPATH"]

if __name__ == "__main__":
    with open(rf"C:\{user}\OneDrive - P.ARC AG\data.json", encoding="utf-8") as file:
        jf = json.load(file)
        d = {}
        for a in jf:
            sid = a["shortId"]
            d[sid] = a
        write_file = open(rf"C:\{user}\OneDrive - P.ARC AG\by_short_id.json", encoding="utf-8", mode="w")
        json.dump(d, write_file, ensure_ascii=False, indent=3)
        write_file.close()


def get_numbers():
    num_affairs_by_legislative_period = {}
    num_affairs_by_party = {}
    num_tokens_by_party = {}

    with open(rf"C:\{user}\OneDrive - P.ARC AG\data.json", encoding="utf-8") as f:
        json_file = json.load(f)
        for affair in json_file:
            if "councillor" in affair["author"].keys() and "party" in affair["author"]["councillor"].keys():
                legislative_period = affair["deposit"]["legislativePeriod"]
                party = affair["author"]["councillor"]["party"]
                if party in interested_parties:
                    if legislative_period in num_affairs_by_legislative_period.keys():
                        num_affairs_by_legislative_period[legislative_period] += 1
                    else:
                        num_affairs_by_legislative_period[legislative_period] = 1

                    if party in num_affairs_by_party.keys():
                        num_affairs_by_party[party] += 1
                    else:
                        num_affairs_by_party[party] = 1

                    num_tokens = 0
                    for text in affair["texts"]:
                        if "tagged" in text.keys():
                            num_tokens = len(text["tagged"]["Lemmas"])

                    if party in num_tokens_by_party.keys():
                        num_tokens_by_party[party] += num_tokens
                    else:
                        num_tokens_by_party[party] = num_tokens

    return num_affairs_by_party, num_tokens_by_party, num_affairs_by_legislative_period


def get_affair_by_shortid(shortid):
    with open(rf"C:\{user}\OneDrive - P.ARC AG\by_short_id.json", encoding="utf-8", mode="r") as func_file:
        json_data = json.load(func_file)
        return json_data[shortid]


def get_details_by_cname(name):
    with open("JSON/councillor_details.json", "r") as func_file:
        json_data = json.load(func_file)
        return json_data[name]


def trim_rule(word, count, min_count):
    if count > 100:
        return gensim.utils.RULE_DISCARD
    else:
        return gensim.utils.RULE_DEFAULT


def calculate_accuracy(dictionary):
    correct = 0
    total = 0

    for person, data in dictionary.items():
        actual_party = data['Zugehörigkeit']
        similarities = data['Ähnlichkeiten']

        # Find the parties with the two highest similarities
        predicted_parties = sorted(similarities, key=similarities.get, reverse=True)[:1]

        # If one of the predicted parties is the same as the actual party, increment correct
        if actual_party in predicted_parties:
            correct += 1

        total += 1

    # Calculate accuracy
    accuracy = correct / total

    return accuracy


def get_num_councillors(party):
    with open(rf"JSON/councillor_details.json", encoding="windows-1252") as f:
        json_data = json.load(f)
        data = {}
        for councillor in json_data:
            if json_data[councillor]["party"] in data.keys():
                data[json_data[councillor]["party"]] += 1
            else:
                data[json_data[councillor]["party"]] = 1

        return data[party]


def tag_text(cleaned_text):
    tagger = treetaggerwrapper.TreeTagger(
        TAGLANG='de',
        TAGPARFILE=r"C:\TreeTagger\lib\german.par",
        TAGABBREV=r"C:\TreeTagger\lib\german-abbreviations"
    )
    tags = treetaggerwrapper.make_tags(tagger.tag_text(cleaned_text))
    out_dict = {"Words": [], "Tags": [], "Lemmas": []}
    try:
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
    except:
        pass

    return out_dict


def clean_text(text_raw):
    text = ''
    doc = nlp(text_raw)
    clean = [token for token in doc if not
    token.is_punct and not token.is_digit and not token.is_currency
             and not token.is_bracket and len(token.text) > 1 and token not in STOP_WORDS]
    for token in clean:
        text += token.text.lower().replace(';</p><p>-', ' ').replace('</p>', ' ').replace('<p>', ' ').replace('</p',
                                                                                                              ' ').replace(
            '/p><p', ' ') + " "
    return text
