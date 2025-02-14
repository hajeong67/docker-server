from django.urls import path
from .views import LoginPageView
from django.views.generic import TemplateView

app_name = "users"

urlpatterns = [
    path('login/', LoginPageView.as_view(), name='login'),
    path('index/', TemplateView.as_view(template_name="index.html"), name='index_page'),
]