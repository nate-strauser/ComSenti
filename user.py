import os
import datetime
import logging as log
from datetime import datetime
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from models import *

class MainHandler(webapp.RequestHandler):
    def get(self):
    
        sent_vals = Sentiment.all().filter('value !=', float(0))
        log.debug("Sentiments total %s", sent_vals.count())
        date_vals = {}
      
        for sent in sent_vals:
            if sent.date is None:
                date = datetime.now().strftime("%Y-%m-%d %H")
            else:
                date = sent.date.strftime("%Y-%m-%d %H")
            if date not in date_vals:
                date_vals[date]=sent.value
            else:
                #perform a simple average but should be weighted
                date_vals[date]=(date_vals[date]+sent.value)/2
        
        js_vals = "["
        first = True
        for date, val in date_vals.iteritems():
            if first:
                first = False
            else:
               js_vals += ','
            js_vals += '[\'' + date + '\',' + str(val) + ']'
        js_vals += "]"
        
        template_values = {
            'js_vals': js_vals
            }
            
        path = os.path.join(os.path.dirname(__file__), 'templates/user.html')
        self.response.out.write(template.render(path, template_values))
    
class DataLoader(webapp.RequestHandler):
    def get(self):
        c1_a = Company(name="Apple", refresh_url="?since_id=0&q=&ors=apple+mac")
        c1_a.put()
        c1_b = Company(name="Starbucks", refresh_url="?since_id=0&q=&ors=SBUX+starbucks")
        c1_b.put()
        w1 = Word(word="bad", value=-2)
        w1.put()
        s1 = Sentiment(company=c1_a, date=datetime.now(), value=4.0, source="http://twtter.com/1234", tweet="blah blah")
        s1.put()
        s3 = Sentiment(company=c1_a, date=datetime(2010,10,04,20,30), value=3.0, source="http://twtter.com/1235")
        s3.put()
        s2 = Sentiment(company=c1_b, date=datetime.now(), value=3.0, source="http://twtter.com/5678", tweet="yada yada")
        s2.put()
        self.response.out.write('Done')

class WordsLoader(webapp.RequestHandler):
    def get(self):

        #load the adjectives file into the database 
        for x in open(os.path.realpath('./data/adjectives.dat')):
            #split the file at the EOL
            x = x.replace('\n', '')    

            w = x[0:x.find(':')].replace(':', '')      
            v = x[x.find(':'):len(x)].replace(':', '').replace(' ', '') 
       
            w1 = Word(word=w, value=int(v))
            w1.put()

        self.response.out.write('Done')

class CompanyLoader(webapp.RequestHandler):
    def get(self):

        c1_a = Company(name="Apple", refresh_url="?since_id=0&q=&ors=apple+mac")
        c1_a.put()
        c1_b = Company(name="Starbucks", refresh_url="?since_id=0&q=&ors=SBUX+starbucks")
        c1_b.put()
        self.response.out.write('Done')
        

def main():
    application = webapp.WSGIApplication([
                                 ('/', MainHandler),
                                 ('/load/', DataLoader),
                                                                                ('/words/', WordsLoader),
                                                                                ('/company/', CompanyLoader)
                                ],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()

