from .models import Wheel
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PostWheelModelSerializer
from rest_framework import serializers, status
from drf_spectacular.utils import extend_schema, OpenApiTypes
from .forms import WheelUploadForm
from rest_framework.permissions import IsAuthenticated

class UploadWheelSerializer(serializers.Serializer):
    whl_file = serializers.FileField()

class UploadWheelAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        summary="Get the upload form structure",
        description="Retrieve the structure of the wheel upload form.",
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request, *args, **kwargs):
        form = WheelUploadForm()
        return Response(
            {
                "message": "Upload form retrieved successfully.",
                "fields": {field.name: str(field) for field in form},  # 폼 필드 정보 제공
                "wheel": None,
                "file_url": None,
            },
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Upload a wheel file",
        description="Upload a .whl file to extract and save its metadata.",
        request=UploadWheelSerializer,
        responses={
            201: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
        },
    )

    def post(self, request, *args, **kwargs):
        serializer = UploadWheelSerializer(data=request.data)
        if serializer.is_valid():
            whl_file = serializer.validated_data['whl_file']
            wheel_instance = Wheel.objects.create(whl_file=whl_file)
            wheel_instance.save()
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
