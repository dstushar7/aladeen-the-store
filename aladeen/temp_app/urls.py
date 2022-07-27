from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('world/',views.say_hello)
]