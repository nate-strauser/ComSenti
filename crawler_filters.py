import logging as log

class RetweetFilter:
    def doFilter(self, search_result_list):
        log.debug("Called RetweetFilter... not implemented")
        
class AdvertisementFilter:
    def doFilter(self, search_result_list):
        log.debug("Called AdvertisementFilter... not implemented")
        
class ProfanityFilter:
    def doFilter(self, search_result_list):
        log.debug("Called ProfanityFilter... not implemented")
        
class FilterSetFactory:
    @staticmethod
    def createFilterSet():
        filter_set = FilterSet()
        filter_set.addFilter(RetweetFilter())
        filter_set.addFilter(AdvertisementFilter())
        filter_set.addFilter(ProfanityFilter())
        return filter_set
        
class FilterSet(object):
    filter_list = []
    def addFilter(self, filter):
        self.filter_list.append(filter)
        
    def applyFilters(self, search_result_list):
        for filter in self.filter_list: 
            filter.doFilter(search_result_list) 
