# Toying with asset mindsets
from __future__ import print_function
import os.path
import tinydb

ROOT = os.path.join(os.path.dirname(__file__), "DB_Test.db")

db = tinydb.TinyDB(ROOT, indent=4)
# db.insert({"one":"two","Three":"four"})
print(db.search(tinydb.where("one") == "two"))
doc = db.get(tinydb.where("one") == "two")
print(type(doc))

class DB(tinydb.TinyDB):


class Entity(object):
    def __init__(s, db, doc=None):
        s.db = db
        s.doc = doc or {}
        s.id = None if doc is None else doc.doc_id
    def _update(s, key, value):
        s.doc["name"] = value
        if s.id is None:
            s.id = s.db.insert({"name":value}, doc_id=s.doc.doc_id)
        s.db.update({"name":value}, doc_id=s.doc.doc_id)
    def name():
        def fget(s):
            return s.doc.get("name", "")
        def fset(s, value):
            s._update("name", value)
        return locals()
    name = property(**name())
    def type():
        def fget(s):
            return s.doc.get("type", "")
        def fset(s, value):
            s._update("type", value)
        return locals()
    type = property(**name())
