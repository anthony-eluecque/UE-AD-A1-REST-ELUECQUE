from typing_extensions import TypedDict

class Error(TypedDict):
   code: int
   message: str

ERRORS: dict[str, Error] = {
   "USER_NOT_FOUND": {
      "code": 404,
      "message": "User not found"
   },
   "BOOKINGS_NOT_FOUND": {
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