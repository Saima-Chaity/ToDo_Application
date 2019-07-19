from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:todo_id>/edit/', views.edit, name='edit'),
]
