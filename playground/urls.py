from django.urls import path
from . import views
from .views import get_story


urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_user, name="logout"),
    path('profile/', views.profile_user, name="profile_user"),
    

    path('search_story/', views.search_story, name="search_story"),
    path('api/', get_story, name='get_story')
    # path('request_story/', views.request_story)
]