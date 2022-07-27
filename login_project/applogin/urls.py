from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('signup',views.signup,name="signup"),
    path('login',views.login_user,name="login"),
    path('logout',views.logout_user,name="logout"),
    path('activate/<uid64>/<token>',views.activate,name="activate"),
    path('setsession',views.setsession,name="setsession"),
    path('getsession',views.getsession,name="getsession"),
    path('index',views.login_user,name="index"),
    ]