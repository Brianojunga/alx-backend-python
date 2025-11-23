# messaging_app/middleware.py
from datetime import datetime
from django.http import JsonResponse

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


class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to the messaging app outside
    6:00 AM - 9:00 PM.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now()
        current_hour = now.hour  # 0-23

        # Allow access only between 6 AM and 9 PM
        if current_hour < 6 or current_hour >= 21:
            return JsonResponse(
                {"error": "Messaging app is closed. Access allowed only from 6AM to 9PM."},
                status=403
            )

        response = self.get_response(request)
        return response
    

class RolepermissionMiddleware:
    """
    Middleware to restrict access to certain actions based on user role.
    Only 'admin' or 'moderator' users are allowed.
    """

    ALLOWED_ROLES = ["admin", "moderator"]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        # Only check authenticated users
        if user.is_authenticated:
            user_role = getattr(user, "role", None)

            # Deny access if role is not allowed
            if user_role not in self.ALLOWED_ROLES:
                return JsonResponse(
                    {"error": "Forbidden: You do not have permission to perform this action."},
                    status=403
                )
        else:
            # Deny access for unauthenticated users
            return JsonResponse(
                {"error": "Authentication required."},
                status=401
            )

        response = self.get_response(request)
        return response