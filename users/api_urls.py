from django.urls import path
from .api_views import LogoutAPIView

app_name = "users_api"

urlpatterns = [
    path('logout/', LogoutAPIView.as_view(), name='api_logout'),
]