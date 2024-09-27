from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

SHOWTIMES_URL = "http://127.0.0.1:3202"

PORT = 3201
HOST = '0.0.0.0'

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

@app.route("/bookings", methods=['GET'])
def get_json():
   res = make_response(jsonify(bookings), 200)
   return res

@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_for_user(userid):
   for booking in bookings:
      if str(booking["userid"]) == str(userid):
         res = make_response(jsonify(booking),200)
         return res
   return make_response(jsonify({"error":"Bad input parameter"}),400)

@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_byuser(userid):
   req = request.get_json()

   url = SHOWTIMES_URL + "/showtimes/" + req["date"]
   response = requests.get(url).json()
   # TODO: CHECK STATUS RESPONSE LATER


   # TODO: ADD ID MOVIES TO MATCHING USER ID

   for booking in bookings:
      for date in booking["dates"]:
         if date['date'] == str(response['date']):
            for movieId in date['movies']:
               if movieId == req['movieid']:
                  return make_response({"error": "An existing item already exists"},409)          
   
   return make_response(jsonify(req),200)

def write(bookings):
    data =  {
      "bookings" : bookings
    }
    with open('{}/databases/movies.json'.format("."), 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
