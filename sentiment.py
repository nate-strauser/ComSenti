import logging as log
import re
import datetime
from google.appengine.ext.webapp import template
from models import *

from plugins.base import SENTIMENTS, init_plugins

#inspired from Calculator plugin
class end_token(object):
  lbp = 0

#parsing and expressions:
#  http://effbot.org/zone/simple-top-down-parsing.htm#function-calls  
def tokenize(program):
  for number, operator in re.findall("\s*(?:(\d+)|(\*\*|.))", program):
      if operator in SENTIMENTS:
          yield SENTIMENTS[operator]()
      else:
          raise SyntaxError("unknown operator: %r" % operator)
  yield end_token()
  
def analyze(program, text):
  global token
  global modtext
  next = tokenize(program).next
  token = next()
  
  t = token
  log.debug("send text for analysis: %s", text)
  value = t.led(text)
  modtext = t.modtext

  #return the modified text and the sentiment value to the caller
  return value, modtext

class SentimentAnalyzer:
    def analyze_and_track(self, company, source, text, date):

        value = 0
        init_plugins(text)
        value, modtext = analyze("+", text)

        #multiple operators for the same text
        #x = calculate("-", text)
        #un-comment for local development
        #return value
        #if value == 0:
        #  modtext = ""

        if value <> 0:  
          log.debug("text %s", modtext)  
          log.debug("value %s", value)    
        
        sent = Sentiment(company=company, value=float(value), source=source, tweet=modtext, date=date)
        sent.put()
      
