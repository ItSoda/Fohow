from typing import Any
from django.http import HttpResponse

class FirstMiddleWare:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        print("Ready")
        response = self._get_response(request)
        return response
    
    def proccess_exception(self, request, exception):
        return HttpResponse("Exception!")