from django.http import HttpResponseRedirect
from django.conf import settings
import re
from django.contrib import messages
from django.shortcuts import redirect

class AuthRequiredMiddleware:
    #print("middleware executed")

    def __init__(self, get_response):
        self.get_response = get_response
        #print(get_response)
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        #assert hasattr(request, 'user')
        path = request.path_info
        if request.user.is_authenticated:
            if path == '/register/':
                messages.error(
                    request,
                    "You need to logout first if you want to create another account,",
                )
                return redirect('home')
            if path == '/login/':
                messages.warning(
                    request,
                    "You are already logged in,",
                )
                return redirect('/')
        else:
            if path == '/posts/new/':
                messages.error(
                    request,
                    "You need to login to do that",
                )
                return redirect('login')