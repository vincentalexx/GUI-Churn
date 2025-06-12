from django.urls import path
from . import views

urlpatterns = [
    path('', views.existing_data, name='existing_data'),
    path('new-customer', views.new_data, name='new_data'),
]