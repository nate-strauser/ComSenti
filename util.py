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
		word_db = Word.all().filter("word = ", word).get()
		if word_db is None:
			word_db = Word(word=word, value=int(value))
		else:
			word_db.word=word
			word_db.value=int(value)
		word_db.put()

def loadTerm(company, text, display_text):
	term = Term.all().filter("company = ", company).filter("text = ", text).get()
	if term is None:
		term = Term(company=company, text=text, display_text=display_text)
	else:
		term.display_text = display_text
	term.put()

def loadFalseTerm(company, text):
	term = FalseTerm.all().filter("company = ", company).filter("text = ", text).get()
	if term is None:
		term = FalseTerm(company=company, text=text)
		term.put()

def loadCompany(name):
	comp = Company.all().filter("name = ", name).get()
	if comp is None:
		comp = Company(name=name)
		comp.put()
	return comp

def load_companies():
	apple = loadCompany("Apple")
	
	loadTerm(apple, "apple", "Apple")
	loadTerm(apple, "aapl", "AAPL")
	loadTerm(apple, "mac", "Mac")
	loadTerm(apple, "ipod", "iPod")
	loadTerm(apple, "ipad", "iPad")
	loadTerm(apple, "iphone", "iPhone")
	loadTerm(apple, "imac", "iMac")
	loadTerm(apple, "macbook", "Macbook")
	
	loadFalseTerm(apple, "apple pie")
	loadFalseTerm(apple, "apple cider")
	loadFalseTerm(apple, "apple juice")
	loadFalseTerm(apple, "apple caramel")
	loadFalseTerm(apple, "candy apple")
	loadFalseTerm(apple, "big apple")
	loadFalseTerm(apple, "breakfast")
	loadFalseTerm(apple, "dinner")
	loadFalseTerm(apple, "mac n cheese")
	loadFalseTerm(apple, "mac and cheese")
	loadFalseTerm(apple, "big mac")
	
	google = loadCompany("Google")
	
	loadTerm(google, "google", "Google")
	loadTerm(google, "goog", "GOOG")
	loadTerm(google, "gmail", "Gmail")
	loadTerm(google, "adwords", "AdWords")
	loadTerm(google, "youtube", "YouTube")
		
	for company in Company.all():
		company.query = None
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

