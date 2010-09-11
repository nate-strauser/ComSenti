#!/usr/bin/env python

import logging as log
import urllib
from django.utils import simplejson as json
from google.appengine.api import urlfetch

class TwitterSearch:
    TWITTER_SEARCH_URL_BASE = 'http://search.twitter.com/search.json'

    def execute_search(self, query_text, result_count):
        twitter_search_url = "%s?%s" % (self.TWITTER_SEARCH_URL_BASE, self.create_query_string(query_text, result_count))
        search_results = []
        twitter_response_json = self.fetch(twitter_search_url)
        if not twitter_response_json:
            log.info("No results")
            return None
        search_results.extend(twitter_response_json.get('results'))
        return search_results

    def create_query_string(self, search_string, result_count):
        query_string = {'q': ('%s' % (search_string)), 'rpp': result_count};
        return urllib.urlencode(query_string)

    def fetch(self, url):
        log.info("Executing %s", url)
        try:
            twitter_response = urlfetch.fetch(url)
            if twitter_response.status_code == 200:
                log.info("Twitter response [%s]", (twitter_response.content)[0:25])
                return json.loads(twitter_response.content)
            else:
                log.error("Http status code [%s] , response [%s]", twitter_response.status_code, twitter_response)
        except urlfetch.Error, e:
            log.error("Could not fetch url [%s] [%s]", url, e)
            return None
    

