from django.urls import path
from . import views
from ludo.views import home 
urlpatterns = [
    path('', home, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
]