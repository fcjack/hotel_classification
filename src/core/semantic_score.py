import json


def _get_possible_match(possible_matches, word, possibilities, match_type):
    for possibility in possibilities:
        list_words = possibility['key'].split()
        if word == list_words[0]:
            list_words.remove(word)
            possible_match = {
                'value': possibility['value'],
                'next_words': list_words,
                'type': match_type
            }
            possible_matches.append(possible_match)


class SemanticScore(object):
    def __init__(self, json_data):
        """
            For the first step to create a SemanticScore instance,
            we will parse the json data received.
            
            We will change the lists of words (Positives, Negatives and Intensifiers) for
            dictionaries, looking for a better performance to access the value of the word.
             
            As we will access the value by key the time to access is constant. 
        :param json_data: 
        """
        data = json.load(json_data)
        self.positive = dict()
        self.negative = dict()
        self.intensifier = dict()
        for current_object in data['positive']:
            self.positive[current_object['phrase']] = current_object['value']
        for current_object in data['negative']:
            self.negative[current_object['phrase']] = current_object['value']
        for current_object in data['intensifier']:
            self.intensifier[current_object['phrase']] = current_object['multiplier']

    def get_possible_matches(self, word):
        positive_possibilities = [{'key': key, 'value': value} for key, value in self.positive.items() if
                                  word in key.split()]
        negative_possibilities = [{'key': key, 'value': value} for key, value in self.negative.items() if
                                  word in key.split()]
        intensifier_possibilities = [{'key': key, 'value': value} for key, value in self.intensifier.items() if
                                     word in key.split()]
        possible_matches = []
        if len(positive_possibilities) > 0:
            _get_possible_match(possible_matches, word, positive_possibilities, "POSITIVE")

        if len(negative_possibilities) > 0:
            _get_possible_match(possible_matches, word, negative_possibilities, "NEGATIVE")

        if len(intensifier_possibilities) > 0:
            _get_possible_match(possible_matches, word, intensifier_possibilities, "INTENSIFIER")

        return possible_matches
