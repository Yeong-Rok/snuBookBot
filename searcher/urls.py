from django.urls import path
from searcher import views

urlpatterns = [
    path('1/', views.room1, name='room1'),
    path('6/', views.room6, name='room6'),
]