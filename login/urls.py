from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('login/', views.login, name="login"),
    path('signin/', views.signin, name="signin"),
    path('', views.main, name="main"),
    path('logout/', views.logout, name="logout"),
    path('findpw/', views.findpw, name="findpw"),
    path('signout/', views.signout, name="signout"),
    path('email/', views.email, name="email"),
]