import os
import datetime
import logging as log
from datetime import datetime
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from models import *


class MainHandler(webapp.RequestHandler):
	def agg_sent(self, date, sent, type):
		agg = Aggregate.all().filter('company =', sent.company).filter('type =', type).filter('date =', date).get()
		if agg is None:
			agg = Aggregate(company=sent.company, value=sent.value, date=date, type=type)
			sent.company.aggregate_count += 1
			sent.company.put()
		else:
			agg.value += sent.value
			agg.item_count += 1
		agg.put()
				
		return agg	
   		
	def get(self):
	
		sents = Sentiment.all().filter('agged =', False)
		log.debug("%s sentiments to be agged", sents.count())
		
		for sent in sents:
			#agg min
			sent.min_agg = self.agg_sent(
				datetime(sent.date.year, sent.date.month, sent.date.day, sent.date.hour, sent.date.minute),
				sent,
				'min')
			
			#agg hour
			sent.hour_agg = self.agg_sent(
				datetime(sent.date.year, sent.date.month, sent.date.day, sent.date.hour),
				sent,
				'hour')
			
			#agg day
			sent.day_agg = self.agg_sent(
				datetime(sent.date.year, sent.date.month, sent.date.day),
				sent,
				'day')
			
			sent.agged = True;
			sent.put()
		self.response.out.write('Done')
      	
	
        

def main():
    application = webapp.WSGIApplication([
                                 ('/aggregate', MainHandler)
                                ],
                                debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()

