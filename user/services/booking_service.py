import requests

BOOKINGS_URL = "http://127.0.0.1:3201"

class BookingService:
    @staticmethod
    def get_user_bookings(user_id : str):
        url = f"{BOOKINGS_URL}/bookings/{user_id}"
        response = requests.get(url)
        return response.json() if response.status_code == 200 else None