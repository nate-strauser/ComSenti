from google.appengine.ext import webapp
from twitter_search import TwitterSearch
from google.appengine.ext.webapp import util
from sentiment import SentimentAnalyzer
from models import *
import random
import datetime

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Crawler executing twitter search for \' turtle \' ')
        twitter_search = TwitterSearch()
        search_results = twitter_search.execute_search("turtle", 10)
        if search_results is None:
            self.response.out.write('Crawler found zero results')
        else:
            self.response.out.write('Crawler found the following results')
            self.response.out.write(search_results)
            #fake for now
            query = Company.all()
            sentiment_analyzer = SentimentAnalyzer()
            for company in query:
            	source = "http://www.twitter.com/tweet/" + str(random.randint(1, 1000000))
            	text = "fake tweet text"
            	date = datetime.datetime.now()
            	sentiment_analyzer.analyze_and_track(company, source, text, date)
            

def main():
    application = webapp.WSGIApplication([('/crawler/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()