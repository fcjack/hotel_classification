import unittest

from core.score_calculator import ScoreCalculatorService


class ScoreCalculatorTest(unittest.TestCase):
    def test_score_sentiment_phrase(self):
        all_phrase = ['Nice decor, reasonably priced, a bit stinky in the lobby but helpful staff, free shuttle '
                      'to/from LAX, and the rooms are clean -- except, my buddy who stayed in the room across from me '
                      'got insect bites all over his leg in the one night we were there, we will going to come back '
                      'another day!! I do not sleep well']
        score_calculator_service = ScoreCalculatorService()
        topic_statistics_by_hotel = score_calculator_service.process_statistics("room", all_phrase, {"HotelID": 123121})
        self.assertEqual(topic_statistics_by_hotel.score, 4)

    def test_score_negative_sentiment_phrase(self):
        all_phrase = ["I not sleep very well and not clean room, I will not going to come back to this hotel"]
        score_calculator_service = ScoreCalculatorService()
        topic_statistics_by_hotel = score_calculator_service.process_statistics("room", all_phrase, {"HotelID": 123121})
        self.assertEqual(topic_statistics_by_hotel.score, -5)

    def test_score_expression_not_found(self):
        all_phrase = ["Looks like it just renovated  room was clean and very comfy  no fridge in my room though ; "
                      "free WiFi and airport shuttle was excellent !", "It was fun and excellent hotel"]
        score_calculator_service = ScoreCalculatorService()
        topic_statistics_by_hotel = score_calculator_service.process_statistics("room", all_phrase, {"HotelID": 123121})
        self.assertEqual(topic_statistics_by_hotel.score, 4)
