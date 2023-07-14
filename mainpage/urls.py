# from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import path
from .views import MainPageView
# from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', MainPageView, name='mainpage'),

]
