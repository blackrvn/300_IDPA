import os
import pickle

import requests
from pyodata.exceptions import HttpError

import swissparlpy as spp
from tqdm import tqdm

from corpora import *


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


def get_business_data(person_lastname, person_firstname):
    try:
        bs = spp.get_data(
            "Business",
            Language="DE",
            SubmittedBy=f"{person_lastname} {person_firstname}",
            SubmissionDate__gt=datetime.fromisoformat("1980-01-01 00:00:00+00:00")
        )
        return bs
    except HttpError:
        return None


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


def load_data(corp, person_obj):
    business_list = get_business_data(person_obj['LastName'], person_obj['FirstName'])
    person_details = get_person_details_by_id(person_obj['ID'])
    for business in business_list:
        try:
            business_id = business['ID']
            # transcript = get_transcript_by_bs_id(business_id)
            corp[business_id] = Affair(business, person_details, None)
            # corp[business_id].clean_text()
            """
            corp[business_id].tag_text(
                TAGLANG='de',
                TAGPARFILE=r"C:\TreeTagger\lib\german.par",
                TAGABBREV=r"C:\TreeTagger\lib\german-abbreviations-utf8"
            )
            """
        except KeyError:
            continue


all_people = spp.get_data("Person", Language='DE', DateOfBirth__gt=datetime.fromisoformat("1950-01-01 00:00:00+00:00"))
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

print("Result by Party:")
print(load_corpora("corpora.pickle").get_affair_by_party("SP"))
