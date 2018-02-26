# Toying with asset mindsets
from __future__ import print_function
import os.path
import tinydb

# ROOT = os.path.join(os.path.dirname(__file__), "DB_Test.db")
#
# db = tinydb.TinyDB(ROOT, indent=4)
# # db.insert({"one":"two","Three":"four"})
# print(db.search(tinydb.where("one") == "two"))
# doc = db.get(tinydb.where("one") == "two")
# print(type(doc))


class DB(tinydb.TinyDB):
    def _load_type(s, type, doc):
        elem = TYPES.get(doc["_type"], Entity)("")
        elem._load_doc(doc)
        return elem
        




class Entity(object):
    def __init__(s, type, name=""):
        s._name = name
        s._type = type
        s._doc = {}
        s._id = None

    def _load_doc(s, doc):
        s._id = doc.doc_id
        s.name = doc.get("_name", "")
        s._type = doc.get("_type", "")

    def insert(s, db):
        s._id = db.insert(s.doc)

    def update(s, db):
        db.update(s.doc, doc_id=s._id)

    @property
    def type(s):
        return s._type

    def name():
        def fget(s):
            return s._name
        def fset(s, value):
            s._name = value
            s.doc["_name"] = value
        return locals()
    name = property(**name())

class Asset(Entity):
    pass

TYPES = {
    "asset": Asset
}
