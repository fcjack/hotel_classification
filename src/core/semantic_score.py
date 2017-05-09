import json


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
