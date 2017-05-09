class TopicStatisticsByHotel(object):
    def __init__(self, hotel_id, topic, score, number_of_sentences):
        self.id = hotel_id
        self.topic = topic
        self.score = score
        self.number_of_sentences = number_of_sentences
        if number_of_sentences > 0:
            self.average = abs(score / number_of_sentences)
        else:
            self.average = 0

    def __str__(self):
        return "HOTEL ID: %s    SCORE: %f  NUMBER OF SENTENCES: %d AVERAGE: %f" % (
            self.id, self.score, self.number_of_sentences, self.average)
