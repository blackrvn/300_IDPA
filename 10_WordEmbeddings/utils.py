import json
import os
import gensim

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
