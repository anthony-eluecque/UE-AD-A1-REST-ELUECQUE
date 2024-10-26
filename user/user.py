from flask import Flask, render_template, request, jsonify, make_response, Response
import requests
import json
from werkzeug.exceptions import NotFound
from typing_extensions import Self
from models import User, Error
from repositories import UserRepository

app = Flask(__name__)

ERRORS: dict[str, Error] = {
   "USER_NOT_FOUND": {
      "code": 404,
      "message": "User not found"
   },
   "MISSING_PARAMETERS": {
      "code": 400,
      "message": "Missing or invalid parameters"
   },
   "INTERNAL_SERVER_ERROR": {
      "code": 500,
      "message": "Internal server error"
   }
}

PORT = 3203
HOST = '0.0.0.0'

class UserController:
   userRepository = UserRepository()

   @app.route("/", methods=['GET'])
   def home() -> Response:
      return "<h1 style='color:blue'>Welcome to the User service!</h1>"

   @app.route("/<userid>",  methods=['GET'])
   def get_user_by_id(userid) -> Response:
      user = UserController.userRepository.get_user_by_id(str(userid))
   
      if (user):
         return make_response(jsonify(user),200)
      return make_response(jsonify(ERRORS["USER_NOT_FOUND"]))
   
   @app.route("/", methods=['POST'])
   def create_user():
      req = request.get_json()
      new_user : User = {
         "id": req["id"],
         "name": req["name"],
         "last_active": req["last_active"]
      }
      UserController.userRepository.create_user(new_user)
      return make_response(jsonify({}),204)

   # TODO
   # /:id/bookings GET 
   # /:id/bookings POST
      
if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   user_controller = UserController()
   app.run(host=HOST, port=PORT)
