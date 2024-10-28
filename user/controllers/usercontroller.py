from flask import Response, jsonify, make_response, request
from repositories import UserRepository
from models import User, ERRORS
from context import bp
import requests
from services import BookingService, MovieService
from dto import BookingDTO

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
      user : User = {
         "id": req["id"],
         "name": req["name"],
         "last_active": req["last_active"]
      }
      UserController.userRepository.create_user(user)
      return make_response(jsonify({}),204)
   
   @bp.route("/<userid>/bookings", methods=['GET'])
   def get_bookings_from_user_id(userid):
      bookings_data = BookingService.get_user_bookings(userid)
         
      if bookings_data:
         bookings = [BookingDTO(**booking) for booking in bookings_data["dates"]]
         return make_response(jsonify([booking.__dict__ for booking in bookings]), 200)
      return make_response(jsonify(ERRORS["BOOKINGS_NOT_FOUND"]), 404)
   
   @bp.route("/<userid>/bookings/<date>/movies")
   def get_movies_details_from_user_bookings(userid,date):
      bookings_data = BookingService.get_user_bookings(userid)
      if not bookings_data:
         return make_response(jsonify(ERRORS["BOOKINGS_NOT_FOUND"]), 404)
      
      bookings = [BookingDTO(**booking) for booking in bookings_data["dates"]]
      movies = []

      for booking in bookings:
         if booking.date == date:
            for movie_id in booking.movies:
               movie = MovieService.get_movie_details(movie_id)
               if movie:
                  movies.append(movie)
               else:
                  return make_response(jsonify(ERRORS["MOVIE_NOT_FOUND"]), 404)
      return make_response(jsonify(movies),200)

   # TODO
   # /:id/bookings POST

