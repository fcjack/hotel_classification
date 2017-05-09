from nltk.tokenize import word_tokenize

from core.semantic_score import SemanticScore
from model.topic_statistics_by_hotel import TopicStatisticsByHotel
from util.file_util import FileUtil

semantic_dir = "../../resources/semantics"


def load_semantic():
    semantic = None
    semantic_file_path = FileUtil.get_file_paths_from_directory(semantic_dir)
    for semantic_file_path in semantic_file_path:
        with open(semantic_file_path) as semantic_data:
            semantic = SemanticScore(semantic_data)
    return semantic


def _check_expressions(words, possible_match, sentence_score_factors, word_index):
    """
        This method will analyze if the possible match received is right with the
        text received in list of words.
        If all words are in the words list and in the same order the expression is a match,
        so the sentence_score_factors array is updated with the expression value in the first
        word of the expression, the another words will received the value 0, that in the operation
        of sum will not affect the result.
        
        :param words: array of words to verify expression
        :param possible_match: possible match with the expression
        :param sentence_score_factors: the array with the factors that were processed
        :param word_index: index for the current word 
    """
    match_expression = True
    for k, next_word in enumerate(possible_match['next_words']):
        if next_word != words[word_index + k + 1]:
            match_expression = False
            break
    if match_expression:
        if sentence_score_factors[word_index] is None:
            sentence_score_factors[word_index] = possible_match
        for k, next_word in enumerate(possible_match['next_words']):
            if sentence_score_factors[word_index + k + 1] is None:
                sentence_score_factors[word_index + k + 1] = {'value': 0, 'type': possible_match['type']}
    return match_expression


class ScoreCalculatorService:
    def __init__(self):
        self.semantic = load_semantic()

    def process_statistics(self, topic, sentences_by_topic, hotel_info):
        """
            This public method is the method that will be called by another class to process the analyze 
            for list of sentences for hotel by topic.
            
            As a result of the process this method will return an instance from TopicStatisticsByHotel
            with the main values for the result.
            
            :param topic: 
            :param sentences_by_topic: 
            :param hotel_info: 
        """
        score_by_hotel = self._calculate_score(sentences_by_topic)
        topic_statistics = TopicStatisticsByHotel(hotel_info['HotelID'], topic, score_by_hotel, len(sentences_by_topic))
        return topic_statistics

    def _calculate_score(self, sentences_by_topic):
        """
            This method will analyze each sentence requesting the score_factor array for each one,
            after received the array with the factors, the specific operation will be executed.
            
            The sentence`s score is the SUM of POSITIVE values plus with respectively INTENSIFIER
             subtracted of SUM of NEGATIVE values plus with respectively INTENSIFIER.
             
             When we are analyzing the words if we have a INTENSIFIER that is more than 2 index difference with
             the current word and the current word is a common word without values to operate, the intensifier
             will be reset for value 1, because the INTENSIFIER value was not referenced for another value and 
             has to be inconsiderate at the moment.
             
            :param sentences_by_topic: List of sentences to analyze 
        """

        score_by_hotel = 0
        for sentence in sentences_by_topic:
            positive = 0
            negative = 0
            intensifier = 1
            intensifier_index = -1
            words = word_tokenize(sentence)
            sentence_score_array = self._get_sentence_score_factors(words)
            for i, score_factor in enumerate(sentence_score_array):
                if score_factor is not None:
                    if score_factor['type'] == "POSITIVE":
                        positive += intensifier * score_factor['value']
                        intensifier = 1
                    elif score_factor['type'] == "NEGATIVE":
                        negative += intensifier * score_factor['value']
                        intensifier = 1
                    else:
                        intensifier *= score_factor['value']
                        intensifier_index = i
                else:
                    if intensifier_index > -1 and (i - intensifier_index) > 2:
                        intensifier = 1
            score_by_hotel += positive - negative

        return score_by_hotel

    def _get_sentence_score_factors(self, words):
        """
            This method will analyze all words OR expressions that we received in a sentence.
            The idea of this method is first analyze word by word, but if a word can have
            many meanings we have to analyze the follow words.
            
            For example, the word NOT can be a INTENSIFIER with the value to multiply -1 and 
            can the same word can start an expression NOT GOING TO COME BACK that has the value
            2 to remove for the score, negative points.
            
            So, this analysis consist in check if the word is a single word value or beginning of
            the expression, if the word has the possibility of the expression we have to check
            all next words to verify if is an expression or not.
            
            In case of the expression all the words of the expression can`t be analyzed again and
            in case of single word, is a simple word value to calculate.
            
            So, this method will generate in the end of process for the list of words, one ARRAY
            with the values and intensifiers for this sentence.
            
            I called this array as sentence_score_factors, that will be processed and summed values
            after.
            
            Example:
            sentence = "I REALLY LIKE THE HOTEL AND IT WAS NICE"
            words = ["I", "REALLY", "LIKE", "THE", "HOTEL", "AND", "IT", "WAS", "NICE"]
            
            sentence_score_facotrs = [None, {"value": 2, "type": "INTENSIFIER", {"value": 1, "type": "POSITIVE"},
            None, None, None, None, None, {"value": 1, "type": POSITIVE}}]
            
            
        :param words: list of words to process 
        """
        sentence_score_factors = [None] * len(words)
        for j, word in enumerate(words):
            if len(word) > 2 and sentence_score_factors[j] is None:
                possible_matches = self.semantic.get_possible_matches(word.lower())
                if len(possible_matches) > 0:
                    if len(possible_matches) > 1:
                        # Sort the possibilities by the length of the next words to check
                        possible_matches.sort(key=lambda match: len(match['next_words']), reverse=True)
                        for i, possible_match in enumerate(possible_matches):
                            result = _check_expressions(words, possible_match, sentence_score_factors, j)
                            if result:
                                break
                    else:
                        if sentence_score_factors[j] is None:
                            if len(possible_matches[0]['next_words']) == 0:
                                sentence_score_factors[j] = possible_matches[0]
                            else:
                                result = _check_expressions(words, possible_matches[0], sentence_score_factors, j)
                                if result:
                                    break

        return sentence_score_factors
