from django.urls import path
from . import views
from .views import UploadWheelTemplateView

app_name = "pypackages"

urlpatterns = [
    path('upload-wheel/', UploadWheelTemplateView.as_view(), name='upload-wheel-template'),
]