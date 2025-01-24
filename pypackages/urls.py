from django.urls import path
from . import views

app_name = "pypackages"

urlpatterns = [
    path('', views.CurrentTimeClassView.as_view(), name='current-time'),
    path('utc/', views.UTCClassView.as_view(), name='utc-time'),
]