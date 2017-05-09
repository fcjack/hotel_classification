# Hotel Classification
This project is a tool that will analyze the hotel`s reviews in resources directory 
and comparing the sentiment described on semantic.json will set a score
for each hotel analyzed.
In the end the user will can see the hotel list ordered by score and
see some information about the process.

# Setup
For setup the project you will need the Python installed in version 3.

For the first step you will need run a the "pip install" for get the dependencies
that are registered on requirements.txt

`pip install -r requirements.txt`

After successfully installed the requirements for the project you
will need download some data for library NLTK.

Open a terminal and input:
`python`

On python console input the following commando:

```

>>> import nltk
>>> nltk.download('punkt')
>>> nltk.download('wordnet')

```

After complete this steps you will have completed the setup process.

# Example

This application is a command line application, for run you will need open a terminal on project root
directory and input:

```
$ python src/main.py <reviews_dir>
```

The parameter ```reviews_dir```  is optional and is the relative path to directory
that will have the data that will be loaded.
The application is waiting for JSON files with a specific model, if the directory parameter
is not specified, the application will use the default directory that is "{projectRoot}/resources/data"

After the execution of this command you will see on terminal something like:
 
 ```
    Welcome to Hotel Classification Tool in Python
    The current relative path to data directory is: ../../resources/data
    Please, enter the topic that you desire classify the hotels: 
 ```
The topic is a word like "room", "breakfast", "bathroom" and this application is waiting only
one word topic, so at the moment is not possible classify for topics with more than one word.
This type of classification can be an improvement in the future.

So, with the default data on the project if you type the topic "room" you will see:

```
1   HOTEL ID: 2514817    SCORE: 395.500000  NUMBER OF SENTENCES: 559 AVERAGE: 0.707513
2   HOTEL ID: 84333      SCORE: 378.000000  NUMBER OF SENTENCES: 690 AVERAGE: 0.547826
3   HOTEL ID: 77923      SCORE: 198.000000  NUMBER OF SENTENCES: 315 AVERAGE: 0.628571
4   HOTEL ID: 81363      SCORE: 144.000000  NUMBER OF SENTENCES: 293 AVERAGE: 0.491468
5   HOTEL ID: 76790      SCORE: 14.000000   NUMBER OF SENTENCES: 24  AVERAGE: 0.583333
Topic [room] processed successfully

```

# Tests

For run tests inside the project you can access on terminal the project root and execute:

```
$ python -m unittest discover -s test/ -p "*_test.py"
```

# Application Design

The hotel classification application analyzes review sentences inside the resources/data directory
to determine the sentiment score for hotel.

At this moment the application received as parameter the directory for data files with these reviews
and in execution time the application need to interact with the user to input some topics that he desire 
to classify the hotels.
 
As a result we will receive the list of hotels with the score, average and number of sentences.

Now I will explain a little more about the approach used on this application.
 
### Sentences

The hotel reviews that we received has a list of reviews of different users with a text that 
analyze the hotel in different aspects, room or breakfast or bathroom and the text can analyze
more than one topic at the same time.

To analyze the user review, we need split this text in sentences that were representing some
review. This is not a trivial task, but for help us with this task, the NLTK library was
utilized.

The NLTK is an amazing library to work with natural language that has great features to work,
like get sentences from text or words from sentence.

If you are interested to learn more about NLTK, I suggest access the web page:
http://www.nltk.org

There you can see the documentation, samples and explanations about the available features.

After that we has the sentences from text we need try to find the sentences that are references for the topic
requested, and we look for the specific word ("topic") inside the sentences and some synonyms or another
forms for the word that can meaning the same topic.

### Words

After the processing for sentences we will have all sentences for hotel that were referencing
the topic, we will need process all words from the sentences to score.
Again, in this time we used NLTK to get all words from the sentence, inside an array.

### Scoring Logic

This is the main part of the project and is not a trivial task to do.
We have a file inside resources directory, semantics.json. In this file we have a group of words and expressions
that are POSITIVE, NEGATIVE or INTENSIFIER category and the value that will increase the score, decrease the score
or multiply the value for one word.

The fact that we can have one word that can start a POSITIVE OR NEGATIVE expression or an INTENSIFIER
word we need analyze the possibilities for each word, we will decrease the performance for the application
but we will increase hits in our application.

One example for this situation of expression or single word is the word "NOT", the word not can be an
INTENSIFIER to multiply -1 or start an expression "NOT GOING TO COME BACK" with value -2.
 
When this cases happens, we will analyze all words for each expression that we received, if they are on sentence
in the exact order we have an expression and we will score the expression value, but if any expression match
we have a single word and will score the word value.

So, to get the score for sentence we will have the following operations:


score = Σ(POSITIVE * INTENSIFIER) - Σ(NEGATIVE * INTENSIFIER)

### Cache Statistics

Looking for increase the performance for user, after process statistics for each topic,
these statistics will be stored inside a dictionary in StatisticsService.
So if you request the same topic again we will not process again if the number of reviews did not change.

If we have the same number of reviews, so we assume that did not change the text.
But in the future we need improve this type of condition, to analyze if the content of the
reviews did not change, to get updated data.

### Future Work

* Include the information about the rating of the hotel and average rating  
* Output more statistics like most positive sentence, or most negative
* Use more feature from NLTK to increase hits on text with another languages too.
* Enable multiple words topic to analyze
* Change the cache structure for a Redis, that will enable control of cache structure
and we will can have more than one application running at the same time reading data from Redis.
