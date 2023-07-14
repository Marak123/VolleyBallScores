from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView

class myLoginView(LoginView):
    template_name = "registration/login.html"
    next_page = "manager:manage"

class myLogoutView(LogoutView):
    # template_name = "registration/login.html"
    next_page = "mainpage:mainpage"