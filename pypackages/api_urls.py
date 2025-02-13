from django.urls import path
from .api_views import UploadWheelAPIView

app_name = "pypackages_api"

urlpatterns = [
    path('wheel/', UploadWheelAPIView.as_view(), name='upload-wheel'),
]