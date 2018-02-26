# Toying with asset mindsets
from __future__ import print_function
import os.path
import tinydb



class Objects(tinydb.database.Table):
    def _load_type(s, type, doc):
        elem = TYPES.get(doc["_type"], Entity)("")
        elem._load_doc(doc)
        return elem
    def get(s, *args, **kwargs):
        res = tinydb.database.Table.get(s, *args, **kwargs)
        return res and s._load_type(res)
    def search(s, *args, **kwargs):
        return [s._load_type(a) for a in tinydb.database.Table.search(s, *args, **kwargs)]

class Entity(object):
    def __init__(s, type, name=""):
        s._doc = {"_type":type, "_name":name}
        s._id = None

    def _load_doc(s, doc):
        s._id = doc.doc_id

    def insert(s, db):
        s._id = db.insert(s._doc)

    def update(s, db):
        db.update(s._doc, doc_id=s._id)

    @property
    def type(s):
        return s._type

    def name():
        def fget(s):
            return s._doc.get(["_name"], "")
        def fset(s, value):
            s._doc["_name"] = value
        return locals()
    name = property(**name())

class Asset(Entity):
    def __init__(s, name=""):
        Entity.__init__(s, "asset", name)
        s._doc["path"] = ""
    def path():
        def fget(s):
            return s._doc.get("path", "")
        def fset(s, value):
            s._doc["path"] = value
        return locals()
    path = property(**path())

def NewDB(*args, **kwargs):
    tinydb.TinyDB.table_class = Objects
    return tinydb.TinyDB(*args, **kwargs)

TYPES = {
    "asset": Asset
}

################################

ROOT = os.path.join(os.path.dirname(__file__), "DB_Test.db")

db = NewDB(ROOT, indent=4)
doc = Asset("my asset")
doc.name = "Asset this!"
doc.path = "Over/there/file"
# print(doc)
# print(dir(db))
doc.insert(db)
# res = db.get(tinydb.where("_name") == "my asset")
# print( res)
# print( type(res))
