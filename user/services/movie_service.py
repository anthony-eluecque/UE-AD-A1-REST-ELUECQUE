import requests
import os 
MOVIE_SERVICE_URL = os.getenv("MOVIE_CLIENT")

class MovieService:
    @staticmethod
    def get_movie_details(movie_id: str):
        url = f"{MOVIE_SERVICE_URL}/movies/{movie_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None