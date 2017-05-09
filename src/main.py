import sys

from core.application import Application
from model.hotel_reviews import HotelReviews
from util.file_util import FileUtil


def main(data_dir="../../resources/data"):
    """
        This main method will receive the directory with the data and will
        try load data to memory as specified as HotelReview model.
        
        After load data will create an Application`s instance that will be used to process
         the files.
    :param data_dir: String (relative path to directory) 
    :return: Application
    """
    print("Welcome to Hotel Classification Tool in Python")
    print("The current relative path to data directory is: %s" % data_dir)
    file_paths = FileUtil.get_file_paths_from_directory(data_dir)
    hotel_reviews = []
    for file_path in file_paths:
        with open(file_path) as json_data:
            hotel_reviews.append(HotelReviews(json_data))
    return Application(hotel_reviews)


if __name__ == '__main__':
    application = None
    if len(sys.argv) == 1:
        application = main()
    elif len(sys.argv) == 2:
        application = main(data_dir=sys.argv[1])
    elif len(sys.argv) > 2:
        raise ValueError('Wrong number of arguments. The argument is "Relative path to data directory"(optional)')

    while True:
        topic = input("Please, enter the topic that you desire classify the hotels: ")
        application.process_topic(topic)
        print("Topic [%s] processed successfully" % topic)
