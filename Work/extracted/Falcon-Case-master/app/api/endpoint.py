from database import db
from database import cache
from database.models import JSONObject
from flask import request
from flask_restplus import Resource, Api, Namespace, fields
from api import utils
from gather import tasks
import json

endpoint_api = Namespace('endpoint', description='Add or retrieve JSON objects to/from the store.')

add = endpoint_api.model('add', {
    'data': fields.String(required=True, description='The JSON object to add to the store.'),
})

retrieve = endpoint_api.model('retrieve', {
    'id': fields.Integer(required=True, description='The ID of the JSON object to retrieve from the store.'),
})

@endpoint_api.route('/<int:id>')
@endpoint_api.param('id', 'The ID of the JSON object to retrieve from the store.')
class EndpointAPI(Resource):
    @endpoint_api.doc("Retrieve the JSON object matching the id from the store.")
    @cache.memoize(60)
    def get(self, id):
        """Retrieve the JSON object matching the id from the store."""
        object = JSONObject.query.get(id)

        if(object): # If we successfully retrieved an object given the identifier, then return success and the object.
            return utils.success_200((object.json_id, object.json_contents))
        else: # Otherwise the object could not be found, so return an error.
            return utils.bad_request_400("Could not find object with id: {}".format(id))

@endpoint_api.route('/')
class EndpointCollectionAPI(Resource):
    @endpoint_api.doc("Retrieve all JSON objects from the store.")
    @cache.cached(60)
    def get(self):
        """Retrieve all JSON objects from the store."""
        store = JSONObject.query.all()
        
        return utils.success_200([(x.json_id, x.json_contents) for x in store])
    
    @endpoint_api.doc("Add new JSON object to the store.")
    @endpoint_api.expect(add)
    def post(self):
        """Add new JSON object to the store."""
        data = request.json
        if(data): # If we have an input we can proceed, otherwise it's a bad request.
            try: # Check if JSON is valid
                _ = json.dumps(data)
            except json.decoder.JSONDecodeError as e: # If it's bad, then it's a bad request.
                return utils.bad_request_400("Bad input.")
        
            tasks.persist_to_db.delay(data)          
            cache.clear() # Invalidate cache, as the data in the cache no longer matches what is in the database.

            return utils.success_200(data) # Return success.
        else:
            return utils.bad_request_400("Missing input.")
        