from django.urls import path, include

urlpatterns = [
    path("", include('lists.urls'), name="lists"),
]
