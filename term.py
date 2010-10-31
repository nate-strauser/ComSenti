import os
import datetime
import logging as log
from datetime import datetime
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from models import *
from google.appengine.api import memcache 


class MainHandler(webapp.RequestHandler):
	def get(self):
	
		sents = Sentiment.all().filter('termed =', False)
		log.debug("%s sentiments to be termed", sents.count())
		
		
		cache_name = 'TERMS'
		terms = memcache.get(cache_name)
		
		if terms is None:
		    terms = Term.all()
		    memcache.set(cache_name, terms, 60*60)
		    log.info('Load cache %s with company terms', cache_name)
				
		for sent in sents:
			text = sent.text.lower()
			for term in terms.filter('company =', sent.company):
				if text.find(term.text) > -1:
					sent.terms.append(term.key())
					term.total_value += sent.value
					term.sentiment_count += 1
					term.average_value = term.total_value / term.sentiment_count
					term.put()
			sent.termed = True;
			sent.put()
		
		self.response.out.write('Done')
      	
	
        

def main():
    application = webapp.WSGIApplication([
                                 ('/term', MainHandler)
                                ],
                                debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()