class JWTTokenCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract token from cookie
        access_token = request.COOKIES.get('access_token')  # use 'access_token' to match  cookie key
        if access_token:
            # Set token Authorization header for DRF
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
        
        # Continue processing
        response = self.get_response(request)
        return response
