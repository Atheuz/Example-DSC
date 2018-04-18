class Config(object):
    SWAGGER_UI_LANGUAGES = ['en']
    SWAGGER_UI_JSONEDITOR = True
    SWAGGER_UI_DOC_EXPANSION = 'list'
    PG_USERNAME = "postgres"
    PG_PASSWORD = "1234"
    PG_DATABASE = "postgres"
    PG_TABLE = "json_table"
    CACHE_TYPE = 'redis'
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@db:5432/{}'.format(PG_USERNAME, PG_PASSWORD, PG_DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = True