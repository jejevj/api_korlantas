from flask import jsonify

def make_response(data=None, message="OK", code=200):
    return jsonify({"code": code, "message": message, "data": data}), code

def ok(data=None, message="OK"): return make_response(data, message, 200)
def created(data=None, message="Created"): return make_response(data, message, 201)
def bad_request(message="Bad Request", data=None): return make_response(data, message, 400)
def not_found(message="Not Found", data=None): return make_response(data, message, 404)
def conflict(message="Conflict", data=None): return make_response(data, message, 409)
def server_error(message="Internal Server Error", data=None): return make_response(data, message, 500)
# New Unauthorized response function
def unauthorized(message="Unauthorized", data=None): return make_response(data, message, 401)