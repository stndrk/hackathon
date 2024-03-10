from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create, name='create'),
    path('update/<int:pk>/', views.update, name='update'),
    path('fetch/', views.fetch, name='get'),
]
