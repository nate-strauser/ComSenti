'''Externally defined basic sentiments for algorithm operations'''import logging as logimport adjectives as adjimport osfrom models import *def register(SENTIMENTS):    SENTIMENTS['+'] = sentiment_positive_token    SENTIMENTS['-'] = sentiment_negative_token    SENTIMENTS['*'] = sentiment_overall_tokenclass sentiment_positive_token(object):    modtext = ""        def nud(self):        return 0    def led(self, text):        #extract dictionary from the database        all_words = Word.all()             #analyze text to get rating value        log.debug("Executing analyzer")        try:            value = 0            #currently just searching for text and adding and subtracting            #but a different mechanism must be implemented that would look for negatives and comparisons            #eliminate from the text the items found so they are not counted again            #for example "not good" and "good" in the same text                        newtext = text            for adjective in all_words:                count = text.count(adjective.word)                if count > 0:                    value = value + count * adjective.value                    #insert special characters around the adjectives to exclude from search                    #also to special format in the UI                    goodadj = '['+adjective.word+']'                    badadj = '{'+adjective.word+'}'                                        if adjective.value > 0:                        newtext = text.replace(adjective.word, goodadj)                    elif adjective.value < 0:                        newtext = text.replace(adjective.word, badadj)            log.debug("Analyzer found a sentiment value of [%s]", value)                        #verify against max and min            if value > 20:                value = 20            elif value < -20:                value = -20            log.debug("After comparing against Maxim, Minim: [%s]", value)            self.modtext = newtext            return value                except Exception, e:            log.error("Error in the counter ", e)            return 0class sentiment_negative_token(object):    def nud(self):        0    def led(self, text):        returnclass sentiment_overall_token(object):    def nud(self):        0    def led(self, text):        return