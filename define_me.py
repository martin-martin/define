# coding: utf-8

import json
from urllib.request import urlopen

### (largely unrelated) owlbot excursion... ###
#with urlopen("https://owlbot.info/api/v1/dictionary/owl") as response:
#    html = response.read()
# should return:
#[{"type":"noun","defenition":"a nocturnal bird of prey with large eyes, a facial disc, a hooked beak, and typically a loud hooting call.","example":"I love reaching out into that absolute silence, when you can hear the owl or the wind."}]

# example search term
search_term = "word"

# interacting with the PEARSON API (Longmans dict for English learners)
# replace "ldoce5" for another dict if applicable:
# http://developer.pearson.com/apis/dictionaries
def query_API(search_term):
    url = "http://api.pearson.com/v2/dictionaries/ldoce5/entries?headword={0}".format(search_term)
    response = urlopen(url)
    # thanks: http://stackoverflow.com/questions/6862770/python-3-let-json-object-accept-bytes-or-let-urlopen-output-strings
    str_response = response.readall().decode('utf-8')
    json_obj = json.loads(str_response)
    return print_entries(json_obj)

# there are often more possible solutions, therefore: iterate
print(json_obj["results"][0]["headword"])
# get the part of speech
print(json_obj["results"][0]["part_of_speech"])
# get the word pronounced
print(json_obj["results"][0]["pronunciations"][0]["audio"][0]["url"]) # iterate
# get the IPA spelling
print(json_obj["results"][0]["pronunciations"][0]["ipa"]) # iterate
# get the definitions
print(json_obj["results"][0]["senses"][0]["definition"][0]) # iterate
# In[46]:

def print_entries(json_obj):
    for headword in json_obj["results"]:
        hw = headword["headword"]
        try:
            pos = headword["part_of_speech"]
        except:
            pos = "_"
        print("{0} | {1}".format(hw, pos))
        try:
            for say in headword["pronunciations"]:
                ipa = say["ipa"]
                print("IPA: {0}".format(ipa))
                for audio in say["audio"]:
                    url = audio["url"]
                    print("URL for voice: http://api.pearson.com{0}".format(url))
        except:
            pass
        try:
            for s in headword["senses"]:
                try:
                    for definition in s["definition"]:
                        print("--def--: {0}".format(definition))
                except: # account for some alternative formats of the API
                    definition = s["signpost"]
                    print("--def--: {0}".format(definition))
                else:
                    pass
        except:
            print("sry, no definition :/")
        print()


query_API("love")
