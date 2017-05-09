import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from core.review_processor import ReviewProcessor
from core.statistics_service import StatisticsService
from core.synonyms_service import SynonymsService
from model.hotel_reviews import HotelReviews
from util.file_util import FileUtil


class StatisticsServiceCache(unittest.TestCase):
    def test_statistcs_service_cache(self):
        review_processor = ReviewProcessor()
        synonym_service = SynonymsService()
        statistic_service = StatisticsService()
        files = FileUtil.get_file_paths_from_directory("../../test/resources")
        hotel_reviews = []
        for file_path in files:
            with open(file_path) as json_data:
                hotel_reviews.append(HotelReviews(json_data))

        synonyms = synonym_service.get_synonym("room")
        statistics = review_processor.process_topic(hotel_reviews[0], "room", synonyms)
        statistic_service.add_statistics_by_topic_and_hotel(hotel_reviews[0].hotel_info, "room", statistics)

        statistics_from_cache = statistic_service.get_statistics_by_topic_and_hotel("room", hotel_reviews[0].hotel_info)
        self.assertEqual(statistics, statistics_from_cache)


if __name__ == '__main__':
    unittest.main()
