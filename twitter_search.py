#!/usr/bin/env python

import logging as log
import urllib
from django.utils import simplejson as json
from google.appengine.api import urlfetch

class TwitterSearch:
    TWITTER_SEARCH_URL_BASE = 'http://search.twitter.com/search.json'
    ##
    # Searches twitter for a search term using the since_id mechanism found the 'refresh_url' key of the json result.
    #  We page through all the results for the current 'refresh_url" then store the 'refresh_url' from the last page for
    #  the next run of the crawler.
    #    @param company: The company.refresh_url field is used to construct the search url. The company.refresh_url is updated
    #        with a current refresh_url.
    #    @return: List of json search results
    def search(self, company):
        search_results = []
        twitter_search_url = "%s%s" % (self.TWITTER_SEARCH_URL_BASE, self.create_query_string(company))
        twitter_response_json = self.fetch(twitter_search_url)
        if not twitter_response_json:
            log.info("No results")
            return None
        search_results.extend(twitter_response_json.get('results'))
        company.since_id = self.create_since_id_from_response(twitter_response_json)
        log.debug("Updating since_id with [%s]" % company.since_id)
        company.put()
        return search_results

    ##
    # Creates the query string for the twitter search URL. The max limit of 100 results is used.
    #    The language is set for English.
    #
    #    @param refresh_url: The refresh_url from a previous run.
    #    @return: The search_string.
    #
    #    @see http://search.twitter.com/api/
    def create_query_string(self, company):
        return '?since_id=%s&q=%s&lang=%s&rpp=%s' % (company.since_id, company.query,'en', '100')
    ##
    # Creates the refresh url
    #
    #    @param twitter_response_url: The twitter json response. Must contain a 'since_id' and 'query' attribute.
    #    @return: the twitter refresh url to be used on subsequent calls.
    def create_since_id_from_response(self, twitter_response_json):
        return int(twitter_response_json.get('max_id'))
    ##
    # Utility: Makes a synchronous request to the twitter search URL.
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
                log.error("Http status code [%s] , response [%s]", twitter_response.status_code, twitter_response.content)
        except urlfetch.Error, e:
            log.error("Could not fetch twitter_search_url [%s] [%s]", twitter_search_url, e)
            return None

    ##
    # Searches twitter for a search term from a start date to an end date. Multiple requests are made to the 
    #    twitter search api until all results are retured. 
    #    
    #    @param search_term:  The search term (string).
    #    @param start_date: The start date in yyyy-mm-dd format (string).
    #    @param end_date: The end date in yyyy-mm-dd format (string).
    #    @return: List of json search results.
    def search_date_range(self, search_term, start_date, end_date):
        search_results = []
        twitter_search_url = "%s?%s" % (self.TWITTER_SEARCH_URL_BASE, self.create_query_string_date_range(search_term, start_date, end_date))
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
    #    The language is set for English.
    #    @deprecated: now using 
    #    @param search_term: The search term.
    #    @param start_date: The start date in yyyy-mm-dd format (string).
    #    @param end_date: The end date in yyyy-mm-dd format (string).
    #    @return: The encoded search_string.
    #
    #    @see http://search.twitter.com/api/
    def create_query_string_date_range(self, search_term, start_date, end_date):
        return 'q=%s&since=%s&until=%s&rpp=%s' % (search_term, start_date, end_date, '100')
