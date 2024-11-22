from flask import Flask, render_template, request, jsonify, make_response
import json
import sys
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'

class Endpoint():
    def __init__(self, path : str, description : str) -> None:
        self.path = path
        self.description = description

ENDPOINTS : dict[str, Endpoint] = {
    "hello_world" : Endpoint('/',"welcome message"),
    "get_all" : Endpoint("/json","get the full JSON database"),
    "get_by_movieid" : Endpoint("/movies/<movieid>", "get the movie by its id"),
    "get_by_movie_title" : Endpoint("/moviesbytitle", "get the movie by its title"),
    "get_by_movie_director" : Endpoint("/moviesbydirector", "get the movie by its director"),
    "get_by_minimum_rating" : Endpoint("/moviesbyminrate", "get the movies with a minimum rate"),
    "create_movie" : Endpoint("/movies/<movieid>", "Adds a movie to the system"),
    "update_rate" : Endpoint("/movies/<movieid>/<rate>", "update a movie rate"),
    "delete movie" : Endpoint("/movies/<movieid>", "delete a movie item")
}

with open('{}/databases/movies.json'.format("."), 'r') as jsf:
   movies = json.load(jsf)["movies"]

# root message
@app.route(ENDPOINTS['hello_world'].path, methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>",200)

@app.route("/help", methods=['GET'])
def help_movie():
    json = {}
    for key,endpoint in ENDPOINTS.items():
        json[key] = {
            "path" : endpoint.path,
            "description" : endpoint.description
        }
    
    res = make_response(jsonify(json),200)
    return res

@app.route(ENDPOINTS["get_all"].path, methods=['GET'])
def get_json():
    res = make_response(jsonify(movies), 200)
    return res

@app.route(ENDPOINTS["get_by_movieid"].path, methods=['GET'])
def get_movie_byid(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            res = make_response(jsonify(movie),200)
            return res
    return make_response(jsonify({"error":"Movie ID not found"}),400)

@app.route(ENDPOINTS["get_by_movie_title"].path, methods=['GET'])
def get_movie_bytitle():
    json = ""
    if request.args:
        req = request.args
        for movie in movies:
            if str(movie["title"]) == str(req["title"]):
                json = movie

    if not json:
        res = make_response(jsonify({"error":"movie title not found"}),400)
    else:
        res = make_response(jsonify(json),200)
    return res

@app.route(ENDPOINTS["get_by_movie_director"].path, methods=['GET'])
def get_movie_bydirector():
    json = ""
    if request.args:
        req = request.args
        for movie in movies:
            if str(movie["director"]) == str(req["director"]):
                json = movie

    if not json:
        res = make_response(jsonify({"error":"movie director not found"}),400)
    else:
        res = make_response(jsonify(json),200)
    return res

@app.route(ENDPOINTS["get_by_minimum_rating"].path, methods=['GET'])
def get_movie_by_min_rate():
    if request.args:
        req = request.args
        matching_movies = {'movies':[]}
        for movie in movies:
            if movie["rating"] >= float(req["min"]):
                matching_movies["movies"].append(movie)

    if len(matching_movies["movies"])==0:
        res = make_response(jsonify({"error":"no movies corresponding"}),400)
    else:
        res = make_response(jsonify(matching_movies),200)
    return res

@app.route(ENDPOINTS["create_movie"].path, methods=['POST'])
def create_movie(movieid):
    req = request.get_json()

    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify({"error":"movie ID already exists"}),409)

    movies.append(req)
    write(movies)
    res = make_response(jsonify({"message":"movie added"}),200)
    return res


@app.route(ENDPOINTS["update_rate"].path, methods=['PUT'])
def update_movie_rating(movieid, rate):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movie["rating"] = float(rate)
            write(movies)
            res = make_response(jsonify(movie),200)
            return res

    res = make_response(jsonify({"error":"movie ID not found"}),201)
    return res

@app.route(ENDPOINTS["delete movie"].path, methods=['DELETE'])
def del_movie(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movies.remove(movie)
            write(movies)
            return make_response(jsonify(movie),200)

    res = make_response(jsonify({"error":"movie ID not found"}),400)
    return res

def write(movies):
    data =  {
        "movies" : movies
    }
    with open('{}/databases/movies.json'.format("."), 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    #p = sys.argv[1]
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)
