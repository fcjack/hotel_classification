from datetime import datetime


class StatisticsService:
    def __init__(self):
        self.statistics_by_topic = {}

    def add_statistics_by_topic_and_hotel(self, hotel_info, topic, statistics):
        key = (hotel_info["HotelID"], topic)
        self.statistics_by_topic[key] = (datetime.now(), statistics)

    def get_statistics_by_topic_and_hotel(self, topic, hotel_info):
        now = datetime.now()
        key = (hotel_info["HotelID"], topic)
        if key in self.statistics_by_topic.keys():
            statistics_date = self.statistics_by_topic[key][0]
            difference = now - statistics_date
            if difference.total_seconds() > 60:
                self.statistics_by_topic.pop(key)
                return None
            else:
                return self.statistics_by_topic[key][1]
        return None
