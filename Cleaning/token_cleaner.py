import nltk

import string
import re

#We get el token list in and should process it or something
#Custom reveal is a list of dictionaries with keys {'pattern' : '', 'repl' : '', 'type' : (either 'string_compare' or 'regex')}
#Option to lemmatize tokens
def clean_tokens(
    token_list,
    stopwords = [],
    hyperlinks = True,
    punctuation = True,
    emojis = True,
    custom_removal_list = None,
    lemmatize = True
    ):
    clean_tokens = []
    #Is this a token list or a list of lists?
    #Just a token list I think

    for token in token_list:
        if hyperlinks:
            token = remove_hyperlinks(token = token)

        if punctuation:
            token = remove_punctuation(token = token)

        if emojis:
            token = remove_emojis(token = token)

        if stopwords:
            token = remove_stopwords(token = token, stopwords = stopwords)

        if custom_removal_list:
            token = clear_customs(token = token, custom_removal_list = custom_removal_list)

        if token == "":
            continue

        clean_tokens.append(token)

    clean_tokens = lemmatize_tokens(token_list = clean_tokens)

    return clean_tokens


def clear_customs(token, custom_removal_list):
    for custom_removal in custom_removal_list:
        if custom_removal["type"] == "regex":
            re.sub(pattern = custom_removal['pattern'], repl = custom_removal['repl'], string = token)

        elif custom_removal["type"] == "string_compare":
            token.replace(custom_removal['pattern'], custom_removal['repl'])

    return token


def remove_hyperlinks(token):
    return re.sub(pattern = r"http\S+", repl = "", string = token)


def remove_punctuation(token):
    return "" if token in string.punctuation else token


def remove_stopwords(token, stopwords):
    return "" if token in stopwords else token


def remove_emojis(token):
    if len(token) == 1 and token not in string.printable:
        return ""
    else:
        return token


def remove_non_ascii(token):
    accepted = [string.ascii_letters, string.digits]
    for character in token:
        for match_list in accepted:
            if character in match_list:
                pass
#REMOVE THESE RANDOM ...'s that aren't caught by punc. Catching non-text/digit strings and gutting them.

def lemmatize_tokens(token_list):
    clean_tokens = []
    lemmatizer = nltk.stem.WordNetLemmatizer()

    for token in token_list:
        clean_tokens.append(lemmatizer.lemmatize(token))

    return clean_tokens

