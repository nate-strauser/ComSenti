from google.appengine.ext import db

#Not normalizing the table on purpose. We will have an apple company for each search term and corresponding refresh_url
#To utilize the since_id feature of twitter search we must make single term search queries due to the following twitter bug
# (http://code.google.com/p/twitter-api/issues/detail?id=1154). This forces a row for each search term (i.e. apple, ipod, mac)
# all for the Apple company. I am not normalizing these terms into a "CompanySearchCriteria" table because relationships don't seem
# to be favored in this non-RDBMS database... and articles on the net are leading me to belive that denormalization scales will in GAE.
# http://be.groovie.org/post/296342863/google-datastore-and-the-shift-from-a-rdbms
class Company(db.Model):
    name = db.StringProperty(required=True)
    refresh_url = db.StringProperty(required=True)
    record_count = db.IntegerProperty(required=True, default = 0)
    sentiment_count = db.IntegerProperty(required=True, default = 0)
    aggregate_count = db.IntegerProperty(required=True, default = 0)
    rating = db.FloatProperty(required=True, default = 0.0)

class NotCompany(db.Model):
    name = db.StringProperty(required=True)
    antonym = db.StringProperty(required=True)
 
class Word(db.Model):
    word = db.StringProperty(required=True)
    value = db.IntegerProperty(required=True)

class Record(db.Model):
    company = db.ReferenceProperty(Company, required=True)
    source = db.StringProperty(required=True)
    text = db.StringProperty(multiline=True, required=True)
    date = db.DateTimeProperty(required=True)
    user = db.StringProperty(required=True, default="anonymous")
    user_image_url = db.StringProperty(required=True, default="no image")
    analyzed = db.BooleanProperty(required=True, default = False)

class Aggregate(db.Model):
    company = db.ReferenceProperty(Company, required=True)
    value = db.FloatProperty(required=True, default = 0.0)
    date = db.DateTimeProperty(required=True)
    date_updated = db.DateTimeProperty(required=True, auto_now=True)
    type = db.StringProperty(required=True, choices=set(["min", "hour", "day"]))
    item_count = db.IntegerProperty(required=True, default = 1)
    
class Sentiment(db.Model):
    company = db.ReferenceProperty(Company, required=True)
    text = db.StringProperty(multiline=True, required=False)
    value = db.FloatProperty(required=True, default = 0.0)
    date = db.DateTimeProperty(required=True, auto_now_add=True)
    record = db.ReferenceProperty(Record, required=True)
    agged = db.BooleanProperty(required=True, default = False)
    min_agg = db.ReferenceProperty(Aggregate,
        collection_name="min agg ref")
    hour_agg = db.ReferenceProperty(Aggregate,
        collection_name="hour agg ref")
    day_agg = db.ReferenceProperty(Aggregate,
        collection_name="day agg ref")
    
    
