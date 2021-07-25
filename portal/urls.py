from django.urls import path
from . import views

urlpatterns = [
    #path('', views.open_signup_login_page_view),
    path('', views.login_view),
    #path('main_page', views.open_main_page_view),
    path('main_page', views.pass_python_data_toHTML),
]

