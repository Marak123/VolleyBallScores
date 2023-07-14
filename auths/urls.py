from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import path
from .views import myLoginView, myLogoutView
# from django.contrib.auth.decorators import login_required


urlpatterns = [
    # Expense View
    path('login', myLoginView.as_view(), name='login'),
    path('logout', myLogoutView.as_view(), name='logout'),
]
