from google.appengine.ext import webapp
from twitter_search import TwitterSearch
from crawler_filters import *
from google.appengine.ext.webapp import util
from datetime import datetime
from datetime import tzinfo
from google.appengine.runtime import DeadlineExceededError
from models import *
import logging as log
import time
import random
import datetime


class MainHandler(webapp.RequestHandler):
    def get(self):
        TWITTER_DATETIME_PATTERN = '%a, %d %b %Y %H:%M:%S +0000'
        try:
            twitter_search = TwitterSearch()
            filter_set = FilterSetFactory.createFilterSet()
            company_name = self.request.get('company_name')
            show_table = bool(self.request.get('show_table'))
            query = Company.all()
            query.filter('name =', company_name)
            for company in query:
                
                if show_table:
                	self.response.out.write("<h1>Crawler executing twitter search for [%s], since_id [%s], query [%s]</h1>" % ( company.name, company.since_id, company.query))
                search_result_list = twitter_search.search(company)
                if search_result_list is None:
                    log.info("Crawler found [0] tweets for company [%s] with since_id [%s]" % (company.name, company.since_id))
                    if show_table:
                    	self.response.out.write('<h3>Crawler found zero results</h3>')
                else:
                    log.info("Crawler found [%s] tweets for company [%s] with since_id [%s]" % (len(search_result_list),company.name, company.since_id))
                    if show_table:
                    	self.response.out.write('<h3>Crawler found the following [%s] results</h3>' % len(search_result_list))
                    	self.response.out.write('<table border="0"><tr>')
                    filter_set.applyFilters(search_result_list)
                    for tweet in search_result_list:
                        tweet_date = datetime.datetime.strptime(tweet['created_at'], TWITTER_DATETIME_PATTERN)
                        if show_table:
                        	self.response.out.write('<td><img src="' + tweet['profile_image_url'] + '"></td>')
                        	self.response.out.write('<td><b>' + tweet['from_user'] + '</b></td>')
                        	self.response.out.write('<td><b>' + tweet['created_at'] + '</b></td>')
                        	self.response.out.write('<td>' + tweet['text'] + '</td')
                        	self.response.out.write('</tr><tr>')
                        
                        company.record_count += 1
                        company.put()
                        rec = Record(company=company, source=tweet['source'], text=tweet['text'], date=tweet_date, user=tweet['from_user'], user_image_url=tweet['profile_image_url'])
                        rec.put()
                        
                if show_table:
                	self.response.out.write('</tr></table>')
                else:
                	self.response.out.write('Done')
        except DeadlineExceededError:
            log.error("The crawler could not be completed in time.")

def main():
    application = webapp.WSGIApplication([('/crawler', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
