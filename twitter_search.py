#!/usr/bin/env python

import logging as log
import urllib
from django.utils import simplejson as json
from google.appengine.api import urlfetch

class TwitterSearch:
    TWITTER_SEARCH_URL_BASE = 'http://search.twitter.com/search.json'

    ##
    # Searches twitter for a search term from a start date to an end date. Multiple requests are made to the 
    #    twitter search api until all results are retured. 
    #
    #    @param search_term:  The search term (string).
    #    @param start_date: The start date in yyyy-mm-dd format (string).
    #    @param end_date: The end date in yyyy-mm-dd format (string).
    #    @return: List of json search results.
    def execute_search(self, search_term, start_date, end_date):
        search_results = []
        twitter_search_url = "%s?%s" % (self.TWITTER_SEARCH_URL_BASE, self.create_query_string(search_term, start_date, end_date))
        while(True):
            twitter_response_json = self.fetch(twitter_search_url)
            if not twitter_response_json:
                log.info("No results")
                return None
            search_results.extend(twitter_response_json.get('results'))
            if twitter_response_json.get('next_page'):
                twitter_search_url = "%s%s" % (self.TWITTER_SEARCH_URL_BASE, twitter_response_json.get('next_page'))
                #TODO: remove this break when we are ready to pull pages of results 
                #temporarily only run one loop
                break
            elif twitter_response_json.get('max_id') == -1:
                log.error("search response max_id was -1")
                return None
                break
            else:
                log.debug("search finished without errors.")
                break
        return search_results

    ##
    # Creates the query string for the twitter search URL. The max limit of 100 results is used.
    #    The language is set for english.
    #
    #    @param search_term: The search term.
    #    @param start_date: The start date in yyyy-mm-dd format (string).
    #    @param end_date: The end date in yyyy-mm-dd format (string).
    #    @return: The encoded search_string.
    #
    #    @see http://search.twitter.com/api/
    def create_query_string(self, search_term, start_date, end_date):        
        query_string = {'lang': 'en', 'q': search_term, 'since': start_date, 'until': end_date ,'rpp': 100};
        return urllib.urlencode(query_string)

    ##
    # Makes a synchronous request to the twitter search URL.
    #    @param twitter_search_url: The url to fetch.
    #    @see: http://code.google.com/appengine/docs/python/urlfetch/fetchfunction.html
    def fetch(self, twitter_search_url):
        log.info("Executing %s", twitter_search_url)
        try:
            twitter_response = urlfetch.fetch(twitter_search_url)
            if twitter_response.status_code == 200:
                log.info("Twitter response [%s]", (twitter_response.content)[0:25])
                return json.loads(twitter_response.content)
            else:
                log.error("Http status code [%s] , response [%s]", twitter_response.status_code, twitter_response)
        except urlfetch.Error, e:
            log.error("Could not fetch twitter_search_url [%s] [%s]", twitter_search_url, e)
            return None
