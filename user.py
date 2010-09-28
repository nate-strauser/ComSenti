import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from models import *

class MainHandler(webapp.RequestHandler):
    def get(self):
    
    	sent_vals = Sentiment.all().filter('value !=', float(0))
    	
    	date_vals = {}
    	
    	
    	for sent in sent_vals:
        	date = sent.date.strftime("%m/%d/%Y %H:%M")
        	if date not in date_vals:
        		date_vals[date]=sent.value
        	else:
        		date_vals[date]+=sent.value
        
        
        js_vals = "["	     		
       	first = True
       	for date, val in date_vals.iteritems():
       		if first:
       			first = False
       		else:
       			js_vals += ','
       		js_vals += '[\'{0}\',{1}]'.format(date, val)
        js_vals += "]"
        
        template_values = {
            'js_vals': js_vals
            }
            
        path = os.path.join(os.path.dirname(__file__), 'templates/user.html')
        self.response.out.write(template.render(path, template_values))
    
class DataLoader(webapp.RequestHandler):
    def get(self):
        c1_a = Company(name="Apple", refresh_url="?since_id=0&q=apple")
        c1_a.put()
        c1_b = Company(name="Apple", refresh_url="?since_id=0&q=mac")
        c1_b.put()
        w1 = Word(word="bad", value=-2)
        w1.put()
        s1 = Sentiment(company=c1_a, value=4.0, source="http://twtter.com/1234")
        s1.put()
        s2 = Sentiment(company=c1_b, value=3.0, source="http://twtter.com/5678")
        s2.put()
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

