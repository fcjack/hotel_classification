from nltk.corpus import wordnet as wn


class SynonymsService(object):
    def __init__(self):
        self.synonyms = {
            "staff": ["personnel", "employees", "folks"],
            "bathroom": ["lavatory", "bath", "toilet", "restroom", "washroom", "lavatories", "baths", "shower",
                         "toilets", "restrooms", "washrooms"],
            "room": ["bedroom", "fourth", "quarter", "chamber", "quart", "rooms", "fourths", "quarters", "chambers",
                     "quarters"],
            "hotel": ["inn"]
        }

    def get_synonym(self, word):
        if word in self.synonyms.keys():
            return set(self.synonyms[word])

        synonyms_set = set()
        for key, value in self.synonyms.items():
            if word in value:
                synonyms_set.add(key)
                synonyms_set = synonyms_set.union(set(self.synonyms[key]))
                return synonyms_set

        print("Looking for synonyms for word [%s]" % word)
        synonyms = wn.synsets(word)
        for i, syn in enumerate(synonyms):
            synonyms_set = synonyms_set.union(syn.lemma_names())
        return synonyms_set
