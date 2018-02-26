# Toying with asset mindsets
from __future__ import print_function
import os.path
import tinydb



class Objects(tinydb.database.Table):
    def _load_type(s, doc):
        elem = TYPES.get(doc.get("_type"), Unknown)(s)
        elem._load_doc(doc)
        return elem
    def get(s, *args, **kwargs):
        res = tinydb.database.Table.get(s, *args, **kwargs)
        return res and s._load_type(res)
    def search(s, *args, **kwargs):
        return [s._load_type(a) for a in tinydb.database.Table.search(s, *args, **kwargs)]
    def all(s):
        return [s._load_type(a) for a in tinydb.database.Table.all(s)]
    def new_asset(s, name):
        asset = Asset(s)
        asset.name = name
        return asset

class Entity(object):
    def __init__(s, type, db):
        s._doc = {"_type":type, "_name":""}
        s._id = None
        s._db = db
    def _load_doc(s, doc):
        s._id = doc.doc_id
    def save(s):
        if s._id is None:
            s._id = s._db.insert(s._doc)
        else:
            s._db.update(s._doc, doc_id=s._id)
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

class Unknown(Entity):
    def __init__(s, db):
        Entity.__init__(s, "unknown", db)

class Asset(Entity):
    def __init__(s, db):
        Entity.__init__(s, "asset", db)
        s._doc["path"] = ""
    def path():
        def fget(s):
            return s._doc.get("path", "")
        def fset(s, value):
            s._doc["path"] = value
        return locals()
    path = property(**path())

def DB(*args, **kwargs):
    tinydb.TinyDB.table_class = Objects
    return tinydb.TinyDB(*args, **kwargs)

TYPES = {
    "asset": Asset
}

################################

ROOT = os.path.join(os.path.dirname(__file__), "DB_Test.db")

db = DB(ROOT, indent=4)
asset = db.new_asset("my asset")
asset.name = "Asset this!"
asset.path = "Over/there/file"
asset.save()
res = db.get(tinydb.where("_name") == "my asset")
print(res)
# print( type(res))
