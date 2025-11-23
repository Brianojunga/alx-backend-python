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


# chats/middleware.py
from datetime import datetime, timedelta
from django.http import JsonResponse

class OffensiveLanguageMiddleware:
    """
    Middleware to limit the number of chat messages per IP.
    Example: Max 5 messages per minute.
    """
    MESSAGE_LIMIT = 5  # Max messages
    TIME_WINDOW = 60   # Seconds (1 minute)

    # Track messages per IP
    ip_message_log = {}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)

        # Only track POST requests to the messages endpoint
        if request.method == "POST" and request.path.startswith("/api/messages/"):
            now = datetime.now()
            # Get previous logs for this IP
            if ip not in self.ip_message_log:
                self.ip_message_log[ip] = []
            # Remove old timestamps outside the time window
            self.ip_message_log[ip] = [
                t for t in self.ip_message_log[ip]
                if (now - t).total_seconds() < self.TIME_WINDOW
            ]
            # Check if limit exceeded
            if len(self.ip_message_log[ip]) >= self.MESSAGE_LIMIT:
                return JsonResponse(
                    {"error": "Message limit exceeded. Try again later."},
                    status=429
                )
            # Log this request
            self.ip_message_log[ip].append(now)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Get client IP address from request headers"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
