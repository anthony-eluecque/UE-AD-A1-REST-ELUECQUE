from flask import Flask
from context import bp
import controllers

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.register_blueprint(bp)
   app.run(host=HOST, port=PORT)
