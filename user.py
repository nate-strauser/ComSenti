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
    	company_name = self.request.get('co')
        if company_name is not None:
        	company = Company.all().filter('name = ', company_name).get()
        	
        if company is None:
        	company = Company.all().get()
        	
        	
        int_name = self.request.get('int')
        interval = 'hour'
        interval_format = '%Y-%m-%d %H'
        interval_format_js = '%#m-%#d %#H'
        interval_label = 'Day with Hour'
        if int_name == 'min':
        	interval = int_name
        	interval_format = '%Y-%m-%d %H:%M'
        	interval_format_js = '%#m-%#d %#H:%#M'
        	interval_label = 'Day with Hour and Minute'
        elif int_name == 'day':
        	interval = int_name
        	interval_format = '%Y-%m-%d'
        	interval_format_js = '%#m-%#d'
        	interval_label = 'Day'
        	
        		
        vals = Aggregate.all().filter('type =', interval).filter('company =', company)
        js_vals = "["
        first = True
        for val in vals:
            if first:
                first = False
            else:
               js_vals += ','
            js_vals += '[\'' + val.date.strftime(interval_format) + '\',' + str(val.value) + ']'
        js_vals += "]"
        
        record_count = 0
        sentiment_count = 0
        aggregate_count = 0
        
        for co in Company.all():
        	record_count += co.record_count
        	sentiment_count += co.sentiment_count
        	aggregate_count += co.aggregate_count
        	
        
        template_values = {
            'js_vals': js_vals,
            'cur_company': company,
            'interval': interval,
            'interval_format_js':interval_format_js,
            'interval_label': interval_label,
            'companies': Company.all(),
            'waiting_for_analysis_count': Record.all().filter('analyzed =', False).count(),
            'waiting_for_aggregation_count': Sentiment.all().filter('agged =', False).count(),
            'latest': Record.all().order("-date").filter('company =', company).fetch(20),
            'record_count': record_count,
            'sentiment_count': sentiment_count,
            'aggregate_count': aggregate_count
            }
            
        path = os.path.join(os.path.dirname(__file__), 'templates/user.html')
        self.response.out.write(template.render(path, template_values))
    def post(self):
    	self.get()
        

def main():
    application = webapp.WSGIApplication([
                                 ('/', MainHandler)
                                ],
                                debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()

