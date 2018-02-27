# Toying with asset mindsets
from __future__ import print_function
import os.path
import tinydb

class Factory(tinydb.database.Table):
    def _load_type(s, doc):
        elem = TYPES.get(doc.get("_type"), Unknown)(s)
        elem._load_doc(doc)
        return elem
    def get(s, *args, **kwargs):
        res = super(Factory, s).get(*args, **kwargs)
        print(res)
        print(tinydb.database.Table.get(s, *args, **kwargs))
        return res and s._load_type(res)
    def search(s, *args, **kwargs):
        return [s._load_type(a) for a in super(Factory, s).search(*args, **kwargs)]
    def all(s):
        return [s._load_type(a) for a in super(Factory, s).all()]
    def new_asset(s, name):
        asset = Asset(s, name)
        return asset

class Entity(object):
    def __init__(s, type, db, name):
        s._doc = {"_type":type, "_name":name}
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
        return s._doc.get("_type")
    def name():
        def fget(s):
            return s._doc.get(["_name"], "")
        def fset(s, value):
            s._doc["_name"] = value
        return locals()
    name = property(**name())

class Unknown(Entity):
    def __init__(s, db, name=""):
        super(Unknown, s).__init__("unknown", db, name)

class Asset(Entity):
    def __init__(s, db, name=""):
        super(Asset, s).__init__("asset", db, name)
        s._doc["path"] = ""
    def path():
        def fget(s):
            return s._doc.get("path", "")
        def fset(s, value):
            s._doc["path"] = value
        return locals()
    path = property(**path())

def DB(*args, **kwargs):
    tinydb.TinyDB.table_class = Factory
    return tinydb.TinyDB(*args, **kwargs)

TYPES = {
    "asset": Asset
}

################################

ROOT = os.path.join(os.path.dirname(__file__), "DB_Test.db")
if os.path.exists(ROOT):
    os.unlink(ROOT)

db = DB(ROOT, indent=4)
asset = db.new_asset("my asset")
asset.path = "Over/there/file"
asset.save()
q = tinydb.Query()
print(db.all())
# res = db.get(q.path == "Over/there/file")
# print(res)
