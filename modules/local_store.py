"""
local_store.py
---------------
Minimal file-based collection store, used ONLY when MongoDB is not
configured or not reachable (see modules/config.py::get_db()).
Mimics the tiny subset of the pymongo collection API this app needs:
insert_one, find_one, update_one(..., upsert=True), find.

This exists purely so the application is genuinely runnable out of
the box (requirement: "no fake data, but also must not crash without
a database"). It is NOT a replacement for MongoDB in a real deployment.
"""

import os
import json
import threading
from .config import DATA_DIR

_LOCK = threading.Lock()
_STORE_DIR = os.path.join(DATA_DIR, "local_store")
os.makedirs(_STORE_DIR, exist_ok=True)


class LocalCollection:
    def __init__(self, name):
        self.path = os.path.join(_STORE_DIR, f"{name}.json")
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)

    def _read(self):
        with open(self.path, "r") as f:
            return json.load(f)

    def _write(self, docs):
        with open(self.path, "w") as f:
            json.dump(docs, f, default=str, indent=2)

    def _matches(self, doc, query):
        return all(doc.get(k) == v for k, v in query.items())

    def insert_one(self, doc):
        with _LOCK:
            docs = self._read()
            docs.append(doc)
            self._write(docs)
        return doc

    def find_one(self, query, sort=None):
        docs = self._read()
        matches = [d for d in docs if self._matches(d, query)]
        if sort:
            key, direction = sort[0]
            matches.sort(key=lambda d: d.get(key, ""), reverse=(direction == -1))
        return matches[0] if matches else None

    def find(self, query=None):
        query = query or {}
        docs = self._read()
        return [d for d in docs if self._matches(d, query)]

    def update_one(self, query, update, upsert=False):
        with _LOCK:
            docs = self._read()
            for d in docs:
                if self._matches(d, query):
                    d.update(update.get("$set", {}))
                    self._write(docs)
                    return
            if upsert:
                new_doc = dict(query)
                new_doc.update(update.get("$set", {}))
                docs.append(new_doc)
                self._write(docs)


class LocalDB:
    """Dict-like accessor so callers can do local_db['feedback'] like pymongo."""
    def __getitem__(self, name):
        return LocalCollection(name)
