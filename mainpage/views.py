from django.shortcuts import render
from django.views.generic.detail import DetailView

def MainPageView(request):
    return render(request, 'mainpage/main.html')