from gather import celery
from database import db
from database.models import JSONObject

@celery.task
def persist_to_db(msg):
    obj = JSONObject(contents=msg) # Load into model.
    db.session.add(obj)
    db.session.commit()