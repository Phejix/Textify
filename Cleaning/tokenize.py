import nltk

def tokenize_tweets(string, preserve_case = False, reduce_len = True, strip_handles = True):
    tokenizer = nltk.tokenize.TweetTokenizer(preserve_case = preserve_case, reduce_len = reduce_len, strip_handles = strip_handles)
    return tokenizer.tokenize(string)

