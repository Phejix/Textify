import nltk

class Stopwords(object):
    """
    Include English stopwords as well as add ability to add custom stopwords?
    """
    def __init__(self, languages = [], custom = None):
        self.stopwords = set()

        if languages:
            for language in languages:
                self.stopwords = self.stopwords.union(self.get_language_corpus(language = language))

        if custom:
            self.add_custom_stopwords(custom = custom)


    def get_language_corpus(self, language):
        return set(nltk.corpus.stopwords.words(language))


    def add_custom_stopwords(self, custom):
        self.stopwords = self.stopwords.union(custom)

