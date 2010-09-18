from google.appengine.ext import webapp
from twitter_search import TwitterSearch
from google.appengine.ext.webapp import util
from datetime import datetime
from sentiment import SentimentAnalyzer
from models import *
import random
import datetime

class MainHandler(webapp.RequestHandler):
    def get(self):
        TWITTER_DATETIME_PATTERN = '%a, %d %b %Y %H:%M:%S +0000'
        twitter_search = TwitterSearch()
        sentiment_analyzer = SentimentAnalyzer()
        
        query = Company.all()
        for company in query:
            self.response.out.write('<h1>Crawler executing twitter search for ' + company.name + '</h1>')
            search_results = twitter_search.execute_search(company.name, '2010-09-14', '2010-09-15')
            if search_results is None:
                self.response.out.write('<h3>Crawler found zero results</h3>')
            else:
                self.response.out.write('<h3>Crawler found the following [%s] results</h3>' % len(search_results))
                self.response.out.write('<table border="0"><tr>')
                for tweet in search_results:
                    self.response.out.write('<td><img src="' + tweet['profile_image_url'] + '"></td>')
                    self.response.out.write('<td>' + tweet['from_user'] + '</td>')
                    self.response.out.write('<td>' + tweet['text'] + '</td')
                    self.response.out.write('</tr><tr>')
                    
                    tweet_date = datetime.datetime.strptime(tweet['created_at'], TWITTER_DATETIME_PATTERN)
                    #un-fake/uncomment to start calling the analyzer with live tweet data. For now we just send to the
                    #  browser for convenience.
                    #sentiment_analyzer.analyze_and_track(company, tweet['source'], tweet['text'], tweet_date)
                    
                    #TODO: add tweet['profile_image_url'], tweet['from_user'] to the sentiment
                    #TODO: add tweet['id'] to the sentiment to prevent duplicate sentiment from being added to the db.
                    #  This would not be needed if the crawler runs only once a day to gather yesterday's tweets.
            self.response.out.write('</tr></table>')
            
            #fake for now
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