from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound
import os 

app = Flask(__name__)

SHOWTIMES_URL = os.getenv("SHOWTIME_CLIENT")

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

   if not SHOWTIMES_URL:
      raise ValueError("Showtime url key is required")

   url = SHOWTIMES_URL + "/showtimes/" + req["date"]
   response = requests.get(url)
   showtimes = response.json()

   if response.status_code == 404:
      return make_response(showtimes,404)          

   def get_current_user():
      for booking in bookings:
         if booking["userid"] == userid:
            return booking
      return None
         
   current_user = get_current_user()
   if not current_user : 
      return make_response(jsonify({"error": "User not found"}),404)          

   for booking in bookings:
      for i,date in enumerate(booking["dates"]):
         if date['date'] == str(showtimes['date']):
            for movieId in date['movies']:   
               if movieId == req['movieid']:
                  return make_response({"error": "An existing item already exists"},409)          
   
            if booking == current_user: 
               current_user["dates"][i]["movies"].append(req["movieid"])
               write(bookings)
               return make_response(jsonify(req), 200)

   current_user["dates"].append({
      "date": req["date"],
      "movies": [req["movieid"]]
   })

   write(bookings)
   return make_response(jsonify(req),200)

def write(bookings):
   data =  {
      "bookings" : bookings
   }
   with open('{}/databases/bookings.json'.format("."), 'w') as f:
      json.dump(data, f, indent=2)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
