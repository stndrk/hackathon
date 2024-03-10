from django.urls import path
from . import views
from collaborators import views as collaborator_views

urlpatterns = [
    path('create/', views.create, name='create'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('user_collaborators/', collaborator_views.user_collaborators),
]