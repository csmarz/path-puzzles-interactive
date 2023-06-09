from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/solve', views.solve, name='solve'),
    path('api/case', views.case, name='case')
]