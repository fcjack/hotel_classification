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
        """
            This method is the beginning of the process for the reviews,
            start getting the synonyms from SynonymsService and send the HotelReviews
            to be analyzed.
        :param topic: 
        """
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
        """
            This method will get value from StatisticsService and check if is a valid value.
            If the value is valid, will be returned as processed, because is in cache.
            If the value is None, shows that we need process the reviews for this topic and
            after processed the reviews the statistics will be stored in StatisticsService
        :param topic: 
        :param hotel_review: 
        :param synonyms: 
        """
        statistics = self.statistics_service.get_statistics_by_topic_and_hotel(topic, hotel_review)

        if statistics is None:
            statistics = self.review_processor.process_topic(hotel_review, topic, synonyms)
            self.statistics_service.add_statistics_by_topic_and_hotel(hotel_review, topic, statistics)
            for synonym in synonyms:
                self.statistics_service.add_statistics_by_topic_and_hotel(hotel_review, synonym, statistics)

        return statistics
