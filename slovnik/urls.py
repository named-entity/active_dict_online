from django.urls import path
from . import views

urlpatterns = [
    path('', views.lexeme_list, name='lexeme_list'),
    path('show', views.show_entry, name='show_entry')
]