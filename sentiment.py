import logging as log
from models import *
import random

class SentimentAnalyzer:
    def analyze_and_track(self, company, source, text, date):
        
        #declare dictionaries
        adjectives = {'good': 15, 'nice': 10, 'ok': 5, 'excelent': 20, 'right': 15,
                      'genuine': 15, 'reliable': 17, 'proper': 8, 'favorable': 10, 'best': 20,
                      'quality': 15, 'healthy': 17, 'friend': 17, 'moral': 10, 'happy': 15,
                      
                      'bad': -10, 'worst': -20, 'poor': -5, 'worse': -15, 'horrible': -20,
                      'corrupt': -15, 'atrocious': -20, 'ill': -5, 'criminal': -20, 'wrong': -15,
                      'evil': -20, 'not good': -10, 'detrimental': -9, 'uncomfortable': -15, 'difficult': -15}
        
        #analyze text to get rating value
        log.info("Executing analyzer")
        try:

            value = 0
            
            for k, v in adjectives.iteritems():
               count = text.count(k)
               if count > 0:
                   value = value + count * v

            #verify against max and min
            if value > 20:
                value = 20
            elif value < -20:
                value = -20

            log.info("Analyzer found a sentiment value of [%s]", value)
            #return value
        
        except Exception, e:
            log.error("Error in the counter", e)
            return 0

        
        sent = Sentiment(company=company, value=value, source=source, date=date)
        sent.put()
      
