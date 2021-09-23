from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage),
    path('login', views.login_user),
    path('register', views.register_user),
    path('logout', views.logout_user),

]
