from django.contrib import messages
from django.utils.deprecation import MiddlewareMixin
from .views import view_503


# Mixin for compatibility with Django <1.10
class HandleBusinessExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        return view_503(request)