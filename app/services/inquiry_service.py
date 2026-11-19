from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId
from pymongo import DESCENDING

STATUSES = ("new", "contacted", "booked", "declined")

_FIELDS = (
    "name", "email", "phone", "event_date", "event_type",
    "guest_count", "location", "package", "notes",
)


class InquiryService:
    def __init__(self, db):
        self.collection = db.inquiries

    def create(self, data):
        doc = {field: data.get(field) for field in _FIELDS}
        if doc["event_date"] is not None:
            # Mongo stores datetimes, not dates.
            doc["event_date"] = datetime.combine(doc["event_date"], datetime.min.time())
        doc["status"] = "new"
        doc["created_at"] = datetime.now(timezone.utc)
        result = self.collection.insert_one(doc)
        doc["_id"] = result.inserted_id
        return doc

    def list(self, status=None):
        query = {"status": status} if status in STATUSES else {}
        return list(self.collection.find(query).sort("created_at", DESCENDING))

    def get(self, inquiry_id):
        oid = _to_oid(inquiry_id)
        return self.collection.find_one({"_id": oid}) if oid else None

    def set_status(self, inquiry_id, status):
        if status not in STATUSES:
            raise ValueError(f"Unknown status: {status}")
        oid = _to_oid(inquiry_id)
        if oid is None:
            return False
        result = self.collection.update_one({"_id": oid}, {"$set": {"status": status}})
        return result.matched_count == 1

    def counts(self):
        counts = {status: 0 for status in STATUSES}
        for row in self.collection.aggregate([{"$group": {"_id": "$status", "n": {"$sum": 1}}}]):
            if row["_id"] in counts:
                counts[row["_id"]] = row["n"]
        return counts


def _to_oid(value):
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        return None
