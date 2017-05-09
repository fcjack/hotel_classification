import sys


def main(data_dir="../resources/data"):
    print("Hello Python Project Data Science")
    print("The data directory is: " + data_dir)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    elif len(sys.argv) == 2:
        main(data_dir=sys.argv[1])
    elif len(sys.argv) > 2:
        raise ValueError('Wrong number of arguments. The argument is "Data Directory"(optional)')

    while True:
        topic = input("Please, enter the topic that you desire classify the hotels: ")
        print("Topic [%s] processed successfully" % topic)
