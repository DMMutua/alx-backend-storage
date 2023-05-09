#!/usr/bin/env python3
"""A Module to work with Pymongo"""


from typing import List
from pymongo.collection import Collection


def list_all(mongo_collection: Collection) -> List[dict]:
    """A Function that Lists all Documents in a Mongo Collection"""
    docs = []
    for document in mongo_collection.find():
        docs.append(document)
    return docs
