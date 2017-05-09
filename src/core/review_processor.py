from nltk.tokenize import sent_tokenize

from core.score_calculator import ScoreCalculatorService


def _get_sentences(reviews):
    """
        This function will retorn all sentences that exists on reviews
    :param reviews: 
    :return: 
    """
    all_sentences = []
    for review in reviews:
        sent_tokenize_list = sent_tokenize(review["Content"])
        all_sentences.append(sent_tokenize_list)

    return all_sentences


def _classify_sentence_by_topic(all_sentences_list, topic, synonyms):
    """
        This method will group the sentences that have relation with the topic requested
         or a synonym for the topic
    :param all_sentences_list: 
    :param topic: 
    :param synonyms: 
    """
    topic_sentence = set()

    if len(topic) == 0:
        print("All sentences and points will be analyzed for empty topic")
        for sentence_list in all_sentences_list:
            for sentence in sentence_list:
                topic_sentence.add(sentence)
        return topic_sentence
    else:
        for sentence_list in all_sentences_list:
            for current_sentence in sentence_list:
                if topic in current_sentence:
                    topic_sentence.add(current_sentence)
                else:
                    for synonym in synonyms:
                        if synonym in current_sentence:
                            topic_sentence.add(current_sentence)

    return topic_sentence


class ReviewProcessor(object):
    """
        This class is responsible to process all reviews from hotel received,
        but only reviews that have relation with the topic requested or a synonym
        of the topic
    """

    def __init__(self):
        self.score_calculator = ScoreCalculatorService()

    def process_topic(self, hotel_review, topic, synonyms):
        """
            This is the main method of the class.
            
            This method will process the reviews of the hotel splitting the text of each user
            that reported the review into a sentences list.
            
            For this process I will use the NLTK library to process the text and create sentences,
            looking that the NLTK has a better process of recognize sentences and split correctly,
            so we can guarantee that we will work with the right sentences.
            
            After that we have the sentences of the texts we will classify the sentences if they 
            have the relation with the topic specified by user or some synonym for the word.
            
            In the end of the process we will calculator the hotel`s statistics by topic
            
        :param hotel_review: 
        :param topic: 
        :param synonyms: 
        :return: TopicStatisticsByHotel
        """

        reviews = hotel_review.reviews
        hotel_info = hotel_review.hotel_info
        reviews_sentences = _get_sentences(reviews)
        sentences_by_topic = _classify_sentence_by_topic(reviews_sentences, topic.lower(), synonyms)
        return self.score_calculator.process_statistics(topic, sentences_by_topic, hotel_info)
