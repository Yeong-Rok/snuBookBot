from django.urls import path
from searcher import views

urlpatterns = [
    path('1/', views.room1, name='room1'),
]