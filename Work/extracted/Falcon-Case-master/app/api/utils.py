from flask import jsonify

def bad_request_400(message):
    response = jsonify({'status':'400 Bad Request', 'message':message})
    response.status_code = 400
    return response

def not_found_404(message):
    response = jsonify({'status':'404 Not Found', 'message':message})
    response.status_code = 404
    return response

def internal_server_error_500(message):
    response = jsonify({'status':'500 Internal Server Error.', 'message':message})
    response.status_code = 500
    return response

def success_200(message):
    response = jsonify({'status':'Success', 'message':message})
    response.status_code = 200
    return response