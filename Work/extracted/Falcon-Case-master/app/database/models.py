from sqlalchemy import Column, Integer, JSON
from database import db

class JSONObject(db.Model):
    """Definition of the JSON schema to be used by SQLAlchemy"""

    __tablename__ = 'json_table'
    json_id = Column(Integer, primary_key=True)
    json_contents = Column(JSON)

    def __init__(self, contents=None):
        self.json_contents = contents

    def __repr__(self):
        return '<JSONObject %r>' % (self.json_contents)