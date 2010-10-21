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
                           'current_user': user.nickname()
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


#util 

def load_words():
	for line in open(os.path.realpath('./data/adjectives.dat')):
		line = line.replace('\n', '').replace(' ', '')
		seperator = line.find(':')
		word = line[0:seperator]
		value = line[seperator+1:len(line)]
		log.debug('word:' + word + ' - value:' + value)
		Word(word=word, value=int(value)).put()

def load_companies():
	c1 = Company(name="Apple", refresh_url="?since_id=0&q=&ors=apple+mac")
	c1.put()
	c2 = Company(name="Starbucks", refresh_url="?since_id=0&q=&ors=SBUX+starbucks")
	c2.put()
	#load non company
	c3 = NotCompany(name="Apple", antonym="apple pie")
	c3.put()
	c4 = NotCompany(name="Apple", antonym="apple cider")
        c4.put()
        c5 = NotCompany(name="Apple", antonym="apple juice")
        c5.put()
        c6 = NotCompany(name="Apple", antonym="apple caramel")
        c6.put()
        c7 = NotCompany(name="Apple", antonym="big apple")
        c7.put()

def kill_companies():
    db.delete(Company.all().fetch(500))
    if Company.all().count(500) > 0:
    	kill_companies()  
    
def kill_words():
	db.delete(Word.all().fetch(500))
	if Word.all().count(500) > 0:
		kill_words()  
		
def kill_sentiments():
	db.delete(Sentiment.all().fetch(500))
	if Sentiment.all().count(500) > 0:
		kill_sentiments() 
		
def kill_aggregates():
	db.delete(Aggregate.all().fetch(500))
	if Aggregate.all().count(500) > 0:
		kill_aggregates() 
		
def main():
    application = webapp.WSGIApplication([
                                 ('/util/', MainHandler),
                                 ('/util/killall', KillAll),
                                 ('/util/kill', Kill),
                                 ('/util/loadall', LoadAll),
                                 ('/util/loadwords', WordsLoader),
                                 ('/util/loadcompany', CompanyLoader)
                                 
                                 
                                ],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()

