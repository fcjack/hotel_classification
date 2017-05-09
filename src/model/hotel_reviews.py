import json


class HotelReviews(object):
    def __init__(self, json_data):
        json_file = json.load(json_data)
        self.reviews = json_file['Reviews']
        self.hotel_info = json_file['HotelInfo']
