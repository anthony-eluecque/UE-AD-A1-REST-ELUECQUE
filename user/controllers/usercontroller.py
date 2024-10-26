from flask import Response, jsonify, make_response, request
from repositories import UserRepository
from models import Error, User
from context import bp

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