from flask import Response, jsonify, make_response, request
from repositories import UserRepository
from models import Error, User
from context import bp
import requests

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

BOOKINGS_URL = "http://127.0.0.1:3201"

class UserController:
   userRepository = UserRepository()

   @bp.route("/", methods=['GET'])
   def home() -> Response:
      return "<h1 style='color:blue'>Welcome to the User service!</h1>"

   @bp.route("/<userid>",  methods=['GET'])
   def get_user_by_id(userid) -> Response:
      user = UserController.userRepository.get_user_by_id(str(userid))
   
      if (user):
         return make_response(jsonify(user),200)
      return make_response(jsonify(ERRORS["USER_NOT_FOUND"]))
   
   @bp.route("/", methods=['POST'])
   def create_user() -> Response:
      req = request.get_json()
      new_user : User = {
         "id": req["id"],
         "name": req["name"],
         "last_active": req["last_active"]
      }
      UserController.userRepository.create_user(new_user)
      return make_response(jsonify({}),204)
   
   @bp.route("/<userid>/bookings", methods=['GET'])
   def get_bookings_from_user_id(userid):
      url = BOOKINGS_URL + "/bookings/" + userid
      response = requests.get(url)
      bookings = response.json()
      return make_response(jsonify(bookings),200)
   
   # TODO
   @bp.route("/<userid>/bookings/movies")
   def get_movies_details_from_user_bookings(userid,movieid):
      pass

   # TODO
   # /:id/bookings POST