import os
import datetime
import logging as log
from datetime import datetime
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import users
from models import *
import time

class MainHandler(webapp.RequestHandler):
    def get(self):
    
		path = os.path.join(os.path.dirname(__file__), 'templates/util.html')
		
		user = users.get_current_user()
		if user:
		    logout_url = users.create_logout_url("/")
		
		template_values = {
		                   'logout_url': logout_url,
		                   'current_user': user.nickname(),
		                   'companies': Company.all()
		                   }
		self.response.out.write(template.render(path, template_values))
    
class LoadAll(webapp.RequestHandler):
        
    def get(self):
    	load_words()
        load_companies()
        
        self.response.out.write('Done')

class KillAll(webapp.RequestHandler):
        
    def get(self):
   		
		template_values = {}
		
		path = os.path.join(os.path.dirname(__file__), 'templates/killall.html')
		self.response.out.write(template.render(path, template_values))


class Kill(webapp.RequestHandler):
	def get(self):
		entity = self.request.get('ent')
		
		
		q = db.GqlQuery("SELECT __key__ FROM " + entity)
		db.delete(q.fetch(500))
		
		template_values = {
			'ent': entity,
		    'count': q.count(1)
		    }
		
		path = os.path.join(os.path.dirname(__file__), 'templates/kill.html')
		self.response.out.write(template.render(path, template_values))
		
    
class WordsLoader(webapp.RequestHandler):
    def get(self):
		load_words()
		self.response.out.write('Done')
    
class CompanyLoader(webapp.RequestHandler):
	def get(self):
		load_companies()
		self.response.out.write('Done')

def load_words():
	for line in open(os.path.realpath('./data/adjectives.dat')):
		line = line.replace('\n', '').replace(' ', '')
		seperator = line.find(':')
		word = line[0:seperator]
		value = line[seperator+1:len(line)]
		log.debug('word:' + word + ' - value:' + value)
		Word(word=word, value=int(value)).put()

def load_companies():
	apple = Company(name="Apple")
	apple.put()
	
	Term(company=apple, text="apple", display_text="Apple").put()
	Term(company=apple, text="aapl", display_text="AAPL").put()
	Term(company=apple, text="mac", display_text="Mac").put()
	Term(company=apple, text="ipod", display_text="iPod").put()
	Term(company=apple, text="ipad", display_text="iPad").put()
	Term(company=apple, text="iphone", display_text="iPhone").put()
	Term(company=apple, text="imac", display_text="iMac").put()
	Term(company=apple, text="macbook", display_text="Macbook").put()
	
	FalseTerm(company=apple, text="apple pie").put()
	FalseTerm(company=apple, text="apple cider").put()
	FalseTerm(company=apple, text="apple juice").put()
	FalseTerm(company=apple, text="apple caramel").put()
	FalseTerm(company=apple, text="candy apple").put()
	FalseTerm(company=apple, text="big apple").put()
	FalseTerm(company=apple, text="breakfast").put()
	FalseTerm(company=apple, text="dinner").put()
	FalseTerm(company=apple, text="mac n cheese").put()
	FalseTerm(company=apple, text="mac and cheese").put()
	FalseTerm(company=apple, text="big mac").put()
	
	google = Company(name="Google")
	google.put()
	
	Term(company=google, text="google", display_text="Google").put()
	Term(company=google, text="goog", display_text="GOOG").put()
	Term(company=google, text="gmail", display_text="Gmail").put()
	Term(company=google, text="adwords", display_text="AdWords").put()
	Term(company=google, text="youtube", display_text="YouTube").put()
	
	lockheed = Company(name="Lockheed")
	lockheed.put()
	
	Term(company=lockheed, text="lockheed", display_text="Lockheed").put()
	Term(company=lockheed, text="lmt", display_text="LMT").put()
	Term(company=lockheed, text="f-35", display_text="F-35").put()
	Term(company=lockheed, text="f-22", display_text="F-22").put()
	Term(company=lockheed, text="orion", display_text="Orion").put()
		
		
	verizon = Company(name="Verizon")
	verizon.put()
	
	Term(company=verizon, text="verizon", display_text="Verizon").put()
	Term(company=verizon, text="vz", display_text="VZ").put()
	Term(company=verizon, text="fios", display_text="FIOS").put()
	
	
	comcast = Company(name="Comcast")
	comcast.put()
	
	Term(company=comcast, text="comcast", display_text="Comcast").put()
	Term(company=comcast, text="cmcsa", display_text="CMCSA").put()
	Term(company=comcast, text="xfinity", display_text="xfinity").put()
	
	
	for company in Company.all():
		for term in Term.all().filter('company =', company):
			if company.query is not None:
				company.query += "+OR+"
			else:
				company.query = ""
			company.query += term.text
		company.put()
   
	

def main():
    application = webapp.WSGIApplication([
                                 ('/util/', MainHandler),
                                 ('/util/killall', KillAll),
                                 ('/util/kill', Kill),
                                 ('/util/loadall', LoadAll)
                                 
                                 
                                ],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()

