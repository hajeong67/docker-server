from .models import Wheel
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UploadWheelSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes

class UploadWheelAPIView(APIView):
    authentication_classes = [JWTAuthentication]  # JWT 인증 사용
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 가능
    parser_classes = [MultiPartParser, FormParser]  # 파일 업로드 파서 설정
    @extend_schema(
        summary="Upload a wheel file",
        description="Upload a .whl file via multipart/form-data",
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "whl_file": {
                        "type": "string",
                        "format": "binary",
                        "description": "The .whl file to upload"
                    }
                }
            }
        },
        responses={201: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT},
    )
    def post(self, request, *args, **kwargs):
        serializer = UploadWheelSerializer(data=request.data)

        if serializer.is_valid():
            whl_file = request.FILES['whl_file']
            wheel_instance = Wheel.objects.create(whl_file=whl_file)
            wheel_instance.save()
            return Response(
                {
                    "message": "Wheel uploaded successfully.",
                    "wheel": {"name": wheel_instance.whl_file.name},
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
