from flask_sqlalchemy import SQLAlchemy
import logging
from flask_caching import Cache

db = SQLAlchemy()
cache = Cache(config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://redis:6379/0'})