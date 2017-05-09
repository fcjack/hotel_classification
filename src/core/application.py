from core.review_processor import ReviewProcessor
from core.synonyms_service import SynonymsService


class Application(object):
    def __init__(self, hotel_reviews):
        self.hotel_reviews = hotel_reviews
        self.synonym_service = SynonymsService()
        self.review_processor = ReviewProcessor()

    def process_topic(self, topic):
        statistics_by_hotel = []
        topic = topic.strip()
        synonyms = set()
        if len(topic) > 0:
            synonyms = self.synonym_service.get_synonym(topic)

        for hotel_review in self.hotel_reviews:
            statistics = self.review_processor.process_topic(hotel_review, topic, synonyms)
            statistics_by_hotel.append(statistics)

        statistics_by_hotel.sort(key=lambda current_statistics: current_statistics.score, reverse=True)
        print("Classification for topic: %s" % topic)
        for i, statistics in enumerate(statistics_by_hotel):
            print("%s   %s" % (str(i + 1), str(statistics)))

    def _get_statistics_by_topic(self, topic, hotel_review, synonyms):
        pass
