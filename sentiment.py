import logging as log
from models import *
import random

class SentimentAnalyzer:
    def analyze_and_track(self, company, source, text, date):
        #analyze text to get rating value
        value = random.uniform(-100, 100)
        sent = Sentiment(company=company, value=value, source=source, date=date)
        sent.put()
      
