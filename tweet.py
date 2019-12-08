"""Assignment 1.
"""

import math

# Maximum number of characters in a valid tweet.
MAX_TWEET_LENGTH = 50

# The first character in a hashtag.
HASHTAG_SYMBOL = '#'

# The first character in a mention.
MENTION_SYMBOL = '@'

# Underscore is the only non-alphanumeric character that can be part
# of a word (or username) in a tweet.
UNDERSCORE = '_'

SPACE = ' '

def is_valid_tweet(text: str) -> bool:
    """Return True if and only if and only if text contains between 1 and
    MAX_TWEET_LENGTH characters (inclusive).

    >>>is_valid_tweet('Hello Twitter!')
    True
    >>>is_valid_tweet('')
    False
    >>>is_valid_tweet(2 * 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    False
    """
    
    if 0 < len(text) <= MAX_TWEET_LENGTH:
        return True
    return False

def compare_tweet_lengths(tweet1: str, tweet2: str) -> int:
    """Return 1 if tweet1 is longer than tweet2, Returns
    -1 if tweet1 is shorter than tweet2, Returns 0 if tweet1
    is the same length as tweet2. 
    Precondition: tweet1 is valid and tweet2 is valid.
    
    >>>compare_tweet_lengths("Bye Daniel", "Hello Daniel")
    -1
    >>>compare_tweet_lengths("Hello Daniel", "Bye Daniel")
    1
    >>>compare_tweet_lengths("Hello Daniel", "Hello Daniel")
    0
    """
    
    len_tweet1 = len(tweet1)
    len_tweet2 = len(tweet2)
    
    if len_tweet1 > len_tweet2:
        return 1 
    elif len_tweet1 < len_tweet2:
        return -1 
    return 0

def add_hashtag(tweet: str, word: str)->str:
    """Return string that begins with the tweet, then " ", then HASHTAG_SYMBOL, 
    then the word. 
    Preconditions: tweet is valid and word is valid
    
    >>>add_hashtag("hello world","Blessed")
    "hello world #Blessed"
    >>>add_hashtag("hello world #Blessed","Blessed")
    "hello world #Blessed #Blessed"
    >>>add_hashtag("I like","cscA08")
    "I like #cscA08"
    >>>
    """
    
    potential_tweet = tweet + SPACE + HASHTAG_SYMBOL + word
    if is_valid_tweet(potential_tweet):
        return potential_tweet
    return tweet
    
def contains_helper(symbol: str, tweet: str, word: str)->bool:
    """Return True if symbol concatinated with word is in tweet and 
    Return False if not. 
    Preconditions: symbol is HASHTAG_SYMBOL or MENTION_SYMBOL, tweet is 
    valid and word is valid.
     
    >>>contains_helper("#", "I like #csca08", "csca08")
    True
    >>>contains_helper("#", "I like #csca08", "csc")
    False
    >>>contains_helper("#", "I like #csca08, #mata31", #mata67", "mata31")
    True
    >>>contains_helper("@", "Go @Raptors", "Raptors")
    True
    """
    
    cleaned_tweet = clean(tweet)
    return symbol + word + SPACE in cleaned_tweet + SPACE

def contains_hashtag(tweet: str, word: str)->bool:
    """Return True if and only if the tweet contains the complete hashtagged 
    word and Return False if not.
    Preconditions: Tweet is valid and word is valid.
    
    >>>contains_hashtag("I like #csca08", "csca08")
    True
    >>>contains_hashtag("I like #csca08", "csc")
    False
    >>>contains_hashtag("I like #csca08, #mata31 F, #mata67", "mata31")
    True
    """

    return contains_helper(HASHTAG_SYMBOL, tweet, word)


def is_mentioned(tweet: str, word: str)->bool:
    """Return True if and only if the tweet contains the complete mentioned
    word and Return False if not. 
    Preconditions: tweet is valid and word is valid.
    
    >>>is_mentioned("Go @Raptors", "Raptors")
    True
    >>>is_mentioned("Go @Raptors", "Rapt")
    False
    >>>is_mentioned("Go @Raptors", "Lakers")
    False
    """
    return contains_helper(MENTION_SYMBOL, tweet, word)

def add_mention_exclusive(tweet: str, word: str)->str:
    """Return tweet, then SPACE, then the word if and only if the tweet 
    contains the word and if the word is not already mentioned in tweet. 
    Return tweet if word is mentioned in tweet, if the tweet does not 
    contain the word or in any other case.
    Preconditions: tweet is valid and word is valid.
    
    >>>add_mention_exclusive("Go Raptors", "Raptors")
    "Go Raptors @Raptors"
    >>>add_mention_exclusive("Go Raptors", "Rapt")
    "Go Raptors"
    >>>add_mention_exclusive("Go @Raptors", "Raptors")
    "Go @Raptors"
    """
    
    potential_tweet = tweet + SPACE + MENTION_SYMBOL + word
    is_word_mentioned = is_mentioned(tweet, word)
    tweet_contains_word = SPACE + word + SPACE in SPACE + clean(tweet) + SPACE
    
    if is_word_mentioned or not tweet_contains_word:
        return tweet    
    if is_valid_tweet(potential_tweet): 
        return potential_tweet
    
    return tweet

def num_tweets_required(message: str)->int:
    """Return the minimum numbers of tweets required, considering the
    MAX_TWEET_LENGTH, given the message
    
    >>>num_tweets_required("123456789"*13)
    3
    >>>num_tweets_required("hello")
    1
    """
    
    full_tweets = len(message) // MAX_TWEET_LENGTH
    if len(message) % MAX_TWEET_LENGTH == 0:
        return full_tweets
    return full_tweets + 1
    
def get_nth_tweet(message: str, n: int)->str:
    """Return the nth tweet considering that each tweet has a maximum tweet 
    length of MAX_TWEET_LENGTH. 
    Preconditions: n is an integer greater than 0, and valid nth tweet 
    exists in message.
    
    >>>get_nth_tweet("ABCDEFGHIJ"*6, 2)
    ABCDEFGHIJ
    >>>get_nth_tweet("abcd"*6, 1)
    abcdabcdabcdabcdabcdabcd
    """
    
    index_of_nth_tweet = (n-1) * MAX_TWEET_LENGTH
    if len(message) % MAX_TWEET_LENGTH != 0:
        if len(message[index_of_nth_tweet:len(message)]) < MAX_TWEET_LENGTH:
            return message[index_of_nth_tweet:]
    
    return message[index_of_nth_tweet:index_of_nth_tweet + MAX_TWEET_LENGTH]

def clean(text: str) -> str:
    """Return text with every non-alphanumeric character, except for
    HASHTAG_SYMBOL, MENTION_SYMBOL, and UNDERSCORE, replaced with a
    SPACE, and each HASHTAG_SYMBOL replaced with a SPACE followed by
    the HASHTAG_SYMBOL, and each MENTION_SYMBOL replaced with a SPACE
    followed by a MENTION_SYMBOL.

    >>> clean('A! lot,of punctuation?!!')
    'A  lot of punctuation   '
    >>> clean('With#hash#tags? and@mentions?in#twe_et #end')
    'With #hash #tags  and @mentions in #twe_et  #end'
    """

    clean_str = ''
    for char in text:
        if char.isalnum() or char == UNDERSCORE:
            clean_str = clean_str + char
        elif char == HASHTAG_SYMBOL or char == MENTION_SYMBOL:
            clean_str = clean_str + SPACE + char
        else:
            clean_str = clean_str + SPACE
    return clean_str
