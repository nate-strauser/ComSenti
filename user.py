import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from models import *

class MainHandler(webapp.RequestHandler):
    def get(self):
    
    	
        template_values = {
            'companies': Company.all().order('name'),
            'sentiments': Sentiment.all().order('-date')
            }

        path = os.path.join(os.path.dirname(__file__), 'templates/user.html')
        self.response.out.write(template.render(path, template_values))

class DataLoader(webapp.RequestHandler):
    def get(self):
		c1 = Company(name="Apple", query="apple, ipod, mac")
		c1.put()
		w1 = Word(word="bad", value=-2)
		w1.put()
		s1 = Sentiment(company=c1, value=4.0, source="http://twtter.com/1234")
		s1.put()
        
		self.response.out.write('Done')

def main():
    application = webapp.WSGIApplication([
    										('/', MainHandler),
    									  	('/load/', DataLoader)
    									  ],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
    
    
    
    
