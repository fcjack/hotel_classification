class StatisticsService:
    def __init__(self):
        self.statistics_by_topic = {}

    def add_statistics_by_topic_and_hotel(self, hotel_review, topic, statistics):
        """
            Add the statistics processed on dictionary building a key of dictionary
            with HotelID and Topic
            
        :param hotel_review: 
        :param topic: 
        :param statistics: 
        """
        key = (hotel_review.hotel_info["HotelID"], topic)
        self.statistics_by_topic[key] = (len(hotel_review.reviews), statistics)

    def get_statistics_by_topic_and_hotel(self, topic, hotel_review):
        """
            Get the statistics by topic and hotel, but before return the value
            we check if the number of reviews is different since the time that 
            was processed, if is the same number of reviews we do not need process
            again and return this result.
            
        :param topic: 
        :param hotel_review: 
        """
        key = (hotel_review.hotel_info["HotelID"], topic)
        if key in self.statistics_by_topic.keys():
            number_of_reviews = self.statistics_by_topic[key][0]
            if number_of_reviews != len(hotel_review.reviews):
                self.statistics_by_topic.pop(key)
                return None
            else:
                return self.statistics_by_topic[key][1]
        return None
