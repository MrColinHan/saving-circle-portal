from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view),
    path('logout', views.logout_view, name="logout"),
    path('django_admin', views.goto_admin_view, name='django_admin'),
    path('main_page', views.pass_python_data_toHTML),
    path('download_deposit', views.download_deposit_file),
    path('download_circle', views.download_circle_file)

]

