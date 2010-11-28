import os
import re
import datetime
import time
import logging as log
from datetime import datetime
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from models import *
from plugins.base import SENTIMENTS, init_plugins
import random

class MainHandler(webapp.RequestHandler):
    def get(self):
    
        show_output = bool(self.request.get('show_output'))
        recs = Record.all().filter('analyzed =', False)
        log.debug("%s records to analyze", recs.count())
        random_vals = bool(self.request.get('random_vals'))
        
        false_term_lines = []
        neg_val_lines = []
        pos_val_lines = []
        no_val_lines = []
        
        t1 = time.clock()
        for rec in recs:
            value = 0
	    init_plugins(rec.text)

            #first filter out businesses that do not qualify
	    value, modtext = analyze("X", rec.text, rec.company.name)
            
            line = rec.company.name + ' | ' + rec.text
            #continue with the analysis of the text only if the result is > 1
            if value > 0:

                if random_vals:
                    value = random.randint(-20, 20)
                    modtext = rec.text
                else:
                    value, modtext = analyze("+", rec.text, rec.company.name)
			
                line = line + ' | ' + modtext + ' | ' + str(value)
                
		#multiple operators for the same text
		#x = calculate("-", text)
		#un-comment for local development
		#return value
	 	#if value == 0:
		#  modtext = ""
			
		if value <> 0:  
                    log.debug("text %s", modtext)  
		    log.debug("value %s", value)    
				
		    #only make sent for useful value
		    sent = Sentiment(company=rec.company, text=modtext, value=float(value), record=rec)
		    sent.put()
		    rec.company.total_value += float(value)
		    rec.company.sentiment_count += 1
		    rec.company.average_value = rec.company.total_value / rec.company.sentiment_count
		    rec.company.put()

                    log.debug("Text recorded %s with a rating %s", modtext, value)
                    
                if show_output:
	                if value > 0:
	                    pos_val_lines.append(line+"<BR/>")
	                elif value < 0:
	                    neg_val_lines.append(line+"<BR/>")
	                else:
	                    no_val_lines.append(line+"<BR/>")
		
	    else:
                if show_output:
	            	false_term_lines.append(line+"<BR/>")

            rec.analyzed = True;
	    
	    rec.put()
        
        log.info("Sentiment analysis took %d seconds", time.clock()-t1)   
        path = os.path.join(os.path.dirname(__file__), 'templates/user.html')


        if show_output:
	        self.response.out.write("<B>False Terms</B></br/>")
	        self.response.out.write(false_term_lines)
	        
	        self.response.out.write("</br/>")
	        self.response.out.write("<B>No Values</B></br/>")
	        self.response.out.write(no_val_lines)
	
	        self.response.out.write("</br/>")
	        self.response.out.write("<B>Positive Sentiments</B></br/>")
	        self.response.out.write(pos_val_lines)
	
	        self.response.out.write("</br/>")
	        self.response.out.write("<B>Negative Sentiments</B></br/>")
	        self.response.out.write(neg_val_lines)
        else:
        	self.response.out.write("Done")
        
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
  
def analyze(program, text, company_name):
  global token
  global modtext
  next = tokenize(program).next
  token = next()
  
  t = token
  log.debug("send text for analysis: %s", text)
  value = t.led(text, company_name)
  modtext = t.modtext

  #return the modified text and the sentiment value to the caller
  return value, modtext

def main():
    application = webapp.WSGIApplication([
                                 ('/sentiment', MainHandler)
                                ],
                                debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
   
