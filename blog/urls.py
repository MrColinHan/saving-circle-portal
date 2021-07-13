from django.urls import path
from . import views

urlpatterns = [
    path('', views.pass_python_data_toHTML)
]