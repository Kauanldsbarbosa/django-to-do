from django.urls import path
from lists import views


app_name = "lists"

urlpatterns = [
    path('', views.home_page, name='home'),
    path('lists/new', views.new_list, name='new_list'),
    path('lists/<int:id>/', views.view_list, name='view_list'),
    path('lists/<int:id>/add_item', views.add_item, name='add_item'),
]