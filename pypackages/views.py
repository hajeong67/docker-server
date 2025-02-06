import datetime
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from django.views import View

from .forms import WheelUploadForm
from users.mixins import LoggedInOnlyView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostWheelModelSerializer

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


class CurrentTimeClassView(LoggedInOnlyView, View):
    def get(self, request, *args, **kwargs):
        template_path = 'index.html'
        now = datetime.datetime.now()
        return render(request, template_path, {'time': now})


class UTCClassView(LoggedInOnlyView, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(UTCClassView, self).get_context_data(**kwargs)
        utc_now = datetime.datetime.now(datetime.UTC)
        context.update(
            {
                'time': utc_now,
            }
        )
        return context


# class UploadWheelView(LoggedInOnlyView, View):
#     def get(self, request):
#         form = WheelUploadForm()
#         return render(request, 'upload_wheel.html', {'form': form, 'wheel': None, 'file_url': None})
#
#     def post(self, request):
#         form = WheelUploadForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             wheel_instance = form.save() #모델에서 자동으로 METADATA 처리 후 저장됨
#             return render(request, 'upload_wheel.html', {'form': form, 'wheel': wheel_instance, 'file_url': wheel_instance.whl_file.url})
#
#         else:
#             form.add_error(None, 'Invalid file format. Please upload a valid .whl file.')
#
#         return render(request, 'upload_wheel.html', {'form': form, 'wheel': None, 'file_url': None})


class UploadWheelAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PostWheelModelSerializer(data=request.data)

        if serializer.is_valid():
            wheel_instance = serializer.save()
            return Response(
                {
                    "message": "Wheel uploaded successfully.",
                    "wheel": PostWheelModelSerializer(wheel_instance).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )