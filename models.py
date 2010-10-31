from google.appengine.ext import db

#Not normalizing the table on purpose. We will have an apple company for each search term and corresponding refresh_url
#To utilize the since_id feature of twitter search we must make single term search queries due to the following twitter bug
# (http://code.google.com/p/twitter-api/issues/detail?id=1154). This forces a row for each search term (i.e. apple, ipod, mac)
# all for the Apple company. I am not normalizing these terms into a "CompanySearchCriteria" table because relationships don't seem
# to be favored in this non-RDBMS database... and articles on the net are leading me to belive that denormalization scales will in GAE.
# http://be.groovie.org/post/296342863/google-datastore-and-the-shift-from-a-rdbms
class Company(db.Model):
    name = db.StringProperty(required=True)
    since_id = db.IntegerProperty(required=True, default = 0)
    query = db.StringProperty(required=False)
    record_count = db.IntegerProperty(required=True, default = 0)
    sentiment_count = db.IntegerProperty(required=True, default = 0)
    aggregate_count = db.IntegerProperty(required=True, default = 0)
    total_value = db.FloatProperty(required=True, default = 0.0)
    average_value = db.FloatProperty(required=True, default = 0.0)
    
class Term(db.Model):
    company = db.ReferenceProperty(Company, required=True)
    text = db.StringProperty(required=True)
    display_text = db.StringProperty(required=True)
    sentiment_count = db.IntegerProperty(required=True, default = 0)
    aggregate_count = db.IntegerProperty(required=True, default = 0)
    total_value = db.FloatProperty(required=True, default = 0.0)
    average_value = db.FloatProperty(required=True, default = 0.0)
    
class FalseTerm(db.Model):
    company = db.ReferenceProperty(Company, required=True)
    text = db.StringProperty(required=True)
 
class Word(db.Model):
    word = db.StringProperty(required=True)
    value = db.IntegerProperty(required=True)

class Record(db.Model):
    company = db.ReferenceProperty(Company, required=True)
    source = db.StringProperty(required=True)
    text = db.StringProperty(multiline=True, required=True)
    date = db.DateTimeProperty(required=True)
    user = db.StringProperty(required=False)
    user_image_url = db.StringProperty(required=False)
    analyzed = db.BooleanProperty(required=True, default = False)

class Aggregate(db.Model):
    company = db.ReferenceProperty(Company, required=True)
    term = db.ReferenceProperty(Term, required=False)
    total_value = db.FloatProperty(required=True, default = 0.0)
    average_value = db.FloatProperty(required=True, default = 0.0)
    date = db.DateTimeProperty(required=True)
    js_utc_date = db.StringProperty(required=False)
    date_updated = db.DateTimeProperty(required=True, auto_now=True)
    interval = db.StringProperty(required=True, choices=set(["Minute", "Hour", "Day"]))
    item_count = db.IntegerProperty(required=True, default = 1)
    
class Sentiment(db.Model):
    company = db.ReferenceProperty(Company, required=True)
    text = db.StringProperty(multiline=True, required=False)
    value = db.FloatProperty(required=True, default = 0.0)
    date = db.DateTimeProperty(required=True, auto_now_add=True)
    record = db.ReferenceProperty(Record, required=True)
    termed = db.BooleanProperty(required=True, default = False)
    terms = db.ListProperty(db.Key)
    aggregated = db.BooleanProperty(required=True, default = False)
    aggregates = db.ListProperty(db.Key)
    
    
