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

class Word(db.Model):
    word = db.StringProperty(required=True)
    value = db.IntegerProperty(required=True)
    
class Sentiment(db.Model):
    company = db.ReferenceProperty(Company, required=True)
    value = db.FloatProperty(required=True)
    source = db.StringProperty(required=True)
    text = db.StringProperty(multiline=True)
    date = db.DateTimeProperty()
