
import os.path
import tinydb
import os

db_path = os.path.join(os.path.dirname(__file__), "link.json")

class DB(tinydb.TinyDB):
    def table(s, obj):
        try:
            name = obj.__name__
        except AttributeError:
            name = obj
        table = super(DB, s).table(name)
        table._db = s
        table._obj = obj
        return table

class Factory(tinydb.database.Table):
    def get(s, *args, **kwargs):
        doc = super(Factory, s).get(*args, **kwargs)
        if doc:
            return s._obj(s._db, s, doc)
        return None
    def new(s):
        return s._obj(s._db, s, {})

class Model(object):
    def __init__(s, db, table, doc):
        s._db = db
        s._table = table
        s._doc = doc
        s._id = doc.doc_id if hasattr(doc, "doc_id") else None
    def save(s):
        if s._id:
            return s._table.update(s._doc, doc_id=s._id)
        s._id = s._table.insert(s._doc)
        return s._id
    def id(): # Read only
        def fget(s):
            return s._id
        return locals()
    id = property(**id())

class User(Model):
    def name():
        def fget(s):
            return s._doc.get("name", "")
        def fset(s, value):
            s._doc["name"] = value
        return locals()
    name = property(**name())

class House(Model):
    def people():
        def fget(s):
            return s._db.table(User).all()
        def fset(s, val):
            s._doc["people"] = [a.id for a in val]
        return locals()
    people = property(**people())

if os.path.exists(db_path):
    os.unlink(db_path)

DB.table_class = Factory
db = DB(db_path, indent=4)
users = db.table(User)
user = users.new()
user.name = "stuff"
user.save()
users.clear_cache()
print users.contains(doc_ids=[1])
houses = db.table(House)
house = houses.new()
house.people = [user]
house.save()
print db.table(User).get(doc_id=1)
id = users.insert({"name":"bogus"})
print id, users.get(doc_id=id)
