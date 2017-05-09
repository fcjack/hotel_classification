import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from core.review_processor import ReviewProcessor
from core.synonyms_service import SynonymsService
from model.hotel_reviews import HotelReviews
from util.file_util import FileUtil


class ReviewProcessorTest(unittest.TestCase):
    def test_review_processor_review1(self):
        review_processor = ReviewProcessor()
        synonym_service = SynonymsService()
        files = FileUtil.get_file_paths_from_directory("../../test/resources")
        hotel_reviews = []
        for file_path in files:
            with open(file_path) as json_data:
                hotel_reviews.append(HotelReviews(json_data))

        synonyms = synonym_service.get_synonym("room")
        statistics = review_processor.process_topic(hotel_reviews[0], "room", synonyms)
        self.assertEqual(statistics.score, 198)
        self.assertEqual(statistics.id, '77923')
        self.assertEqual(statistics.number_of_sentences, 315)
        self.assertEqual(statistics.average, abs(198 / 315))


if __name__ == '__main__':
    unittest.main()
