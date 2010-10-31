import os
import datetime
import logging as log
from datetime import datetime
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from models import *


class MainHandler(webapp.RequestHandler):
	def agg_sent(self, date, sent, interval, js_utc_date, term=None):
		agg = Aggregate.all().filter('company =', sent.company).filter('interval =', interval).filter('date =', date)
		
		if term is not None:
			agg = agg.filter('term =', term)
			
		agg = agg.get()
		
		if agg is None:
			agg = Aggregate(company=sent.company, total_value=sent.value, average_value=sent.value, date=date, js_utc_date=js_utc_date, interval=interval, term=term)
			sent.company.aggregate_count += 1
			sent.company.put()
			if term is not None:
				term_ent = db.get(term)
				term_ent.aggregate_count += 1
				term_ent.put()
		else:
			agg.total_value += sent.value
			agg.item_count += 1
			agg.average_value = agg.total_value / agg.item_count
		agg.put()
				
		return agg	
   	
   	def agg_interval(self, sent, interval, term=None):
		
		date = None
		js_utc_date = 'Date.UTC(' + sent.date.strftime("%Y") + ',' + str(int(sent.date.strftime("%m"))-1) + ','  + sent.date.strftime("%d")
		if interval == "Minute":
			date = datetime(sent.date.year, sent.date.month, sent.date.day, sent.date.hour, sent.date.minute)
			js_utc_date += ','  + sent.date.strftime("%H") + ','  + sent.date.strftime("%M")
		elif interval == "Hour":
			date = datetime(sent.date.year, sent.date.month, sent.date.day, sent.date.hour)
			js_utc_date += ','  + sent.date.strftime("%H")
		elif interval == "Day":
			date = datetime(sent.date.year, sent.date.month, sent.date.day)
		js_utc_date += ')'
		
		sent.aggregates.append(self.agg_sent(date, sent, interval, js_utc_date, term).key())	
   		
	def get(self):
	
		sents = Sentiment.all().filter('aggregated =', False).filter('termed =', True)
		log.debug("%s sentiments to be agged", sents.count())
		
		for sent in sents:
			self.agg_interval(sent, 'Minute')
			self.agg_interval(sent, 'Hour')
			self.agg_interval(sent, 'Day')
			
				
			for term in sent.terms:
				self.agg_interval(sent, 'Minute', term)
				self.agg_interval(sent, 'Hour', term)
				self.agg_interval(sent, 'Day', term)
			
			sent.aggregated = True;
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

