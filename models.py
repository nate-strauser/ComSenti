from google.appengine.ext import db

class Company(db.Model):
    name = db.StringProperty(required=True)
    query = db.StringProperty(required=True)
    
class Word(db.Model):
    word = db.StringProperty(required=True)
    value = db.IntegerProperty(required=True)
    
class Sentiment(db.Model):
    company = db.ReferenceProperty(Company, required=True)
    value = db.FloatProperty(required=True)
    source = db.StringProperty(required=True)
    date = db.DateTimeProperty()
