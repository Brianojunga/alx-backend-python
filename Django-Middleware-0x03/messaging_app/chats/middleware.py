# messaging_app/middleware.py
from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the user (AnonymousUser if not authenticated)
        user = request.user if request.user.is_authenticated else "Anonymous"

        # Log the request to a file
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}\n"
        with open("request_logs.txt", "a") as f:
            f.write(log_message)

        # Process the request
        response = self.get_response(request)
        return response
