from django.shortcuts import render
from django.views import View
from users.mixins import LoggedInOnlyView

class UploadWheelTemplateView(LoggedInOnlyView, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'upload_wheel.html', {'user': request.user})  # 로그인된 사용자 정보 전달
