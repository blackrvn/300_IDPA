import os
import pickle
from icecream import ic

import requests
from pyodata.exceptions import HttpError

import swissparlpy as spp
from tqdm import tqdm

from corpora import *


def filter_by_type(ent):
    return spp.filter.and_(
        ent.BusinessType != 1,
        ent.BusinessType != 2,
        ent.BusinessType != 3,
        ent.BusinessType != 4,
        ent.BusinessType != 7,
        ent.BusinessType != 10,
    )


def get_transcript_by_bs_id(business_id):
    ts = spp.get_data(
        table="Transcript",
        Language="DE",
        IdSubject=business_id
    )
    if len(ts) > 0:
        return ts
    else:
        return None


def get_person_id_by_affair_id(affair_id):
    url = f"http://ws-old.parlament.ch/affairs/{affair_id}?lang=de&format=json"
    r = requests.get(url, headers={'Accept': 'application/json'})
    try:
        return r.json()["author"]["councillor"]["id"]
    except:
        return None


def get_person_id_by_name(first_name, last_name):
    ic(first_name, last_name)
    person = spp.get_data("Person",
                          Language="DE",
                          FirstName=first_name,
                          LastName=last_name
                          )
    if person.count == 0:
        person = spp.get_data("Person",
                              Language="DE",
                              FirstName__contains=first_name,
                              LastName__contains=last_name
                              )
    try:
        return person[0]["ID"]
    except:
        return None


def get_business_data(start, end):
    try:
        bs = spp.get_data(
            "Business",
            SubmissionDate__gt=datetime.fromisoformat(f"{start}-01-01 00:00:00+00:00"),
            SubmissionDate__lt=datetime.fromisoformat(f"{end}-01-01 00:00:00+00:00"),
            filter=filter_by_type,
        )
        out_bs = {}
        if bs.count == 0:
            return None
        else:
            for business in bs:
                person_id = get_person_id_by_affair_id(business["ID"])
                if not person_id:
                    if person_id in out_bs.keys():
                        out_bs[''].append(business)
                    else:
                        out_bs[''] = [business]
                else:
                    if person_id in out_bs.keys():
                        out_bs[person_id].append(business)
                    else:
                        out_bs[person_id] = [business]
        return out_bs
    except HttpError:
        return None, None


def get_person_details_by_id(person_id):
    url = f"http://ws-old.parlament.ch:80/councillors/{person_id}?lang=de&format=json"
    r = requests.get(url, headers={'Accept': 'application/json'})
    try:
        return r.json()
    except:
        return None


def load_corpora(path):
    with open(path, 'rb') as file:
        return pickle.load(file)


def dump_corpora(obj, path):
    with open(path, 'wb') as file:
        pickle.dump(obj, file)


def load_data(corp, start, end):
    business_dict = get_business_data(start, end)
    try:
        for person_id, business_lst in business_dict.items():
            try:
                for business in business_lst:
                    business_id = business['ID']
                    person_details = get_person_details_by_id(person_id)
                    # transcript = get_transcript_by_bs_id(business_id)
                    corp[business_id] = Affair(business, person_details, None)
                    corp[business_id].clean_text()
                    corp[business_id].tag_text(
                        TAGLANG='de',
                        TAGPARFILE=r"C:\TreeTagger\lib\german.par",
                        TAGABBREV=r"C:\TreeTagger\lib\german-abbreviations"
                    )
            except KeyError:
                continue
    except AttributeError:
        pass


for date in tqdm(range(1965, 2025), total=2025-1965, desc="Loading..."):
    if os.path.exists("corpora.pickle"):
        corpora = load_corpora("corpora.pickle")

        load_data(corpora, date, date + 1)
        dump_corpora(obj=corpora, path="corpora.pickle")
    else:
        corpora = Corpora()

        load_data(corpora, date, date + 1)
        dump_corpora(obj=corpora, path="corpora.pickle")

"""

all_people = spp.get_data("Person", Language='DE', DateOfBirth__gt=datetime.fromisoformat("1950-01-01 00:00:00+00:00"))
ic(all_people[0])

people = []
for person in tqdm(all_people, total=len(all_people), desc="Filtering..."):
    if get_person_details_by_id(person['ID'])['active']:
        people.append(person)

for person in tqdm(all_people, total=len(all_people), desc="Searching..."):
    if os.path.exists("corpora.pickle"):
        corpora = load_corpora("corpora.pickle")
        load_data(corpora, person)
        dump_corpora(obj=corpora, path="corpora.pickle")
    else:
        corpora = Corpora()
        load_data(corpora, person)
        dump_corpora(obj=corpora, path="corpora.pickle")
        
"""

print("Result by Party:")
print(load_corpora("corpora.pickle").get_affair_by_party("SP"))
