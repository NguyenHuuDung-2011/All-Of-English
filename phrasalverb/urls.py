from django.urls import path
from . import views

urlpatterns = [
    path('/phrasal-verb-table', views.phrasalverb, name='phrasalverb'),
]