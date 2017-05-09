from core.review_processor import ReviewProcessor
from core.statistics_service import StatisticsService
from core.synonyms_service import SynonymsService


class Application(object):
    def __init__(self, hotel_reviews):
        self.hotel_reviews = hotel_reviews
        self.synonym_service = SynonymsService()
        self.review_processor = ReviewProcessor()
        self.statistics_service = StatisticsService()

    def process_topic(self, topic):
        statistics_by_hotel = []
        topic = topic.strip()
        synonyms = set()
        if len(topic) > 0:
            synonyms = self.synonym_service.get_synonym(topic)

        for hotel_review in self.hotel_reviews:
            statistics = self._get_statistics_by_topic(topic, hotel_review, synonyms)
            statistics_by_hotel.append(statistics)

        statistics_by_hotel.sort(key=lambda current_statistics: current_statistics.score, reverse=True)
        print("Classification for topic: %s" % topic)
        for i, statistics in enumerate(statistics_by_hotel):
            print("%s   %s" % (str(i + 1), str(statistics)))

    def _get_statistics_by_topic(self, topic, hotel_review, synonyms):
        statistics = self.statistics_service.get_statistics_by_topic_and_hotel(topic, hotel_review.hotel_info)

        if statistics is None:
            statistics = self.review_processor.process_topic(hotel_review, topic, synonyms)
            self.statistics_service.add_statistics_by_topic_and_hotel(hotel_review.hotel_info, topic, statistics)
            for synonym in synonyms:
                self.statistics_service.add_statistics_by_topic_and_hotel(hotel_review.hotel_info, synonym, statistics)

        return statistics
