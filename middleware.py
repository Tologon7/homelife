from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

class CORSMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == 'OPTIONS':
            response = JsonResponse({'message': 'CORS preflight response'})
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, PATCH, DELETE'
            response['Access-Control-Allow-Headers'] = 'X-CSRFToken, Content-Type, Authorization'
            return response
