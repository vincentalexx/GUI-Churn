from django.urls import path
from . import views

urlpatterns = [
    path('', views.new_data, name='new_data'),
    path('existing_data/', views.existing_data, name='existing_data'),
]