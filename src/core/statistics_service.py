class StatisticsService:
    def __init__(self):
        self.statistics_by_topic = {}

    def add_statistics_by_topic_and_hotel(self, hotel_review, topic, statistics):
        key = (hotel_review.hotel_info["HotelID"], topic)
        self.statistics_by_topic[key] = (len(hotel_review.reviews), statistics)

    def get_statistics_by_topic_and_hotel(self, topic, hotel_review):
        key = (hotel_review.hotel_info["HotelID"], topic)
        if key in self.statistics_by_topic.keys():
            number_of_reviews = self.statistics_by_topic[key][0]
            if number_of_reviews != len(hotel_review.reviews):
                self.statistics_by_topic.pop(key)
                return None
            else:
                return self.statistics_by_topic[key][1]
        return None
