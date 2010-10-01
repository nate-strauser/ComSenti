from google.appengine.ext import webapp
from twitter_search import TwitterSearch
from crawler_filters import *
from google.appengine.ext.webapp import util
from datetime import datetime
from datetime import tzinfo
from sentiment import SentimentAnalyzer
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
            sentiment_analyzer = SentimentAnalyzer()
            filter_set = FilterSetFactory.createFilterSet()
            company_name = self.request.get('company_name')
            query = Company.all()
            query.filter('name =', company_name)
            for company in query:
                self.response.out.write("<h1>Crawler executing twitter search for [%s] </h1>" % ( company.refresh_url))
                search_result_list = twitter_search.search(company)
                log.info("Crawler found [%s] tweets for company [%s] with refresh_url [%s]" % (len(search_result_list),company.name, company.refresh_url))
                if search_result_list is None:
                    self.response.out.write('<h3>Crawler found zero results</h3>')
                else:
                    self.response.out.write('<h3>Crawler found the following [%s] results</h3>' % len(search_result_list))
                    self.response.out.write('<table border="0"><tr>')
                    filter_set.applyFilters(search_result_list)
                    for tweet in search_result_list:
                        tweet_date = datetime.datetime.strptime(tweet['created_at'], TWITTER_DATETIME_PATTERN)
                        self.response.out.write('<td><img src="' + tweet['profile_image_url'] + '"></td>')
                        self.response.out.write('<td><b>' + tweet['from_user'] + '</b></td>')
                        self.response.out.write('<td><b>' + tweet['created_at'] + '</b></td>')
                        self.response.out.write('<td>' + tweet['text'] + '</td')
                        self.response.out.write('</tr><tr>')
                        
                        sentiment_analyzer.analyze_and_track(company, tweet['source'], tweet['text'], tweet_date)
                        #TODO: add tweet['profile_image_url'], tweet['from_user'] to the sentiment
                self.response.out.write('</tr></table>')
        except DeadlineExceededError:
            log.error("The crawler could not be completed in time.")

def main():
    application = webapp.WSGIApplication([('/crawler', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()