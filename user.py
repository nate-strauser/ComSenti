import os
import datetime
import time
import logging as log
from datetime import datetime
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from models import *

class MainHandler(webapp.RequestHandler):
    def get(self):
    	template_values = {
            'companies': Company.all()
        }
            
        path = os.path.join(os.path.dirname(__file__), 'templates/user.html')
        self.response.out.write(template.render(path, template_values))

class RecordsHandler(webapp.RequestHandler):
    def get(self):
    	company_name = self.request.get('co')
        if company_name is not None:
        	company = Company.all().filter('name = ', company_name).get()
        	
        if company is None:
        	company = Company.all().get()
        	
        template_values = {
            'records': Sentiment.all().order("-date").filter('company =', company).fetch(20)
        }
            
        path = os.path.join(os.path.dirname(__file__), 'templates/records.html')
        self.response.out.write(template.render(path, template_values))


class StatusHandler(webapp.RequestHandler):
    def get(self):
    	record_count = 0
        sentiment_count = 0
        aggregate_count = 0
        
        for co in Company.all():
        	record_count += co.record_count
        	sentiment_count += co.sentiment_count
        	aggregate_count += co.aggregate_count
        	
        
        template_values = {
            'waiting_for_analysis_count': Record.all().filter('analyzed =', False).count(),
            'waiting_for_aggregation_count': Sentiment.all().filter('agged =', False).count(),
            'record_count': record_count,
            'sentiment_count': sentiment_count,
            'aggregate_count': aggregate_count
        }
            
        path = os.path.join(os.path.dirname(__file__), 'templates/status.html')
        self.response.out.write(template.render(path, template_values))

class GraphHandler(webapp.RequestHandler):
    def get(self):
    	company_name = self.request.get('co')
        if company_name is not None:
        	company = Company.all().filter('name = ', company_name).get()
        	
        if company is None:
        	company = Company.all().get()
        	
        	
        int_name = self.request.get('int')
        interval = 'min'
        if int_name == 'Hour':
        	interval = 'hour'
        elif int_name == 'Day':
        	interval = 'day'
        		
        vals = Aggregate.all().filter('type =', interval).filter('company =', company)
        js_vals = "["
        first = True
        for val in vals:
            if first:
                first = False
            else:
               js_vals += ','
            js_vals += '[' + val.js_utc_date + ',' + str(val.value) + ']'
        js_vals += "]"
        
        template_values = {
            'js_vals': js_vals,
            'cur_company': company
            }
            
        path = os.path.join(os.path.dirname(__file__), 'templates/graph.js')
        self.response.out.write(template.render(path, template_values))
        

def main():
    application = webapp.WSGIApplication([
                                 ('/', MainHandler),
                                 ('/status', StatusHandler),
                                 ('/records', RecordsHandler),
                                 ('/graph', GraphHandler)
                                ],
                                debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()

