# Toying with asset mindsets
from __future__ import print_function
import os.path
import tinydb

ROOT = os.path.join(os.path.dirname(__file__), "DB_Test.db")

db = tinydb.TinyDB(ROOT, indent=4)
db.insert({"one":"two","Three":"four"})
print(db.search(tinydb.where("one") == "two"))
