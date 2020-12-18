from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',  views.home, name='keygen-home'),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='keygenerator/login.html'),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='keygen-home'),
        name='logout'
    ),
    path('create/', views.create_peer_interface, name='keygen-create'),
]
