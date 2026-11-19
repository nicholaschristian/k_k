import logging

from pymongo import DESCENDING, MongoClient

logger = logging.getLogger(__name__)

_client = None


def init_db(app):
    global _client

    _client = MongoClient(app.config["MONGO_URI"], serverSelectionTimeoutMS=5000)
    db = _client[app.config["MONGO_DBNAME"]]

    ensure_indexes(db)

    app.db = db
    app.mongo_client = _client
    logger.info("Connected to MongoDB database '%s'", app.config["MONGO_DBNAME"])
    return db


def ensure_indexes(db):
    db.inquiries.create_index([("created_at", DESCENDING)])
    db.inquiries.create_index([("status", DESCENDING)])
