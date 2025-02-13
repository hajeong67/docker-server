from django.urls import path
from .api_views import LoginAPIView, LogoutAPIView

app_name = "users_api"

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='api_login'),
    path('logout/', LogoutAPIView.as_view(), name='api_logout'),
]