from google.appengine.ext import webapp
from twitter_search import TwitterSearch
from google.appengine.ext.webapp import util

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Crawler executing twitter search for \' cat \' ')
        twitter_search = TwitterSearch()
        search_results = twitter_search.execute_search("cat", 10)
        if search_results is None:
            self.response.out.write('Crawler found zero results')
        else:
            self.response.out.write('Crawler found the following results')
            self.response.out.write(search_results)

def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()