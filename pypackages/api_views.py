from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from .models import Wheel
from .serializers import UploadWheelSerializer
from rest_framework.parsers import JSONParser
import os
from django.conf import settings

@extend_schema(tags=["pypackages"])
class UploadWheelAPIView(APIView):
    authentication_classes = [JWTAuthentication]  # JWT 인증 사용
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 가능
    parser_classes = [MultiPartParser, FormParser, JSONParser]

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

    @extend_schema(
        summary="Get all wheel files",
        description="Retrieve a list of all uploaded wheel files",
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request, *args, **kwargs):
        wheels = Wheel.objects.all().values("id", "whl_file")
        return Response({"wheels": list(wheels)}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Delete a wheel file",
        description="Delete a specific wheel file by ID",
        parameters=[
            OpenApiParameter(name="id", description="ID of the wheel file", required=True, type=int)
        ],
        responses={204: None, 404: {"error": "Not found"}},
    )
    def delete(self, request, *args, **kwargs):
        wheel_id = request.query_params.get("id")
        if not wheel_id:
            return Response({"error": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            wheel = Wheel.objects.get(id=wheel_id)
            wheel.delete()
            return Response({"message": "Wheel deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Wheel.DoesNotExist:
            return Response({"error": "Wheel file not found"}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        summary="Update a wheel file's name",
        description="Partially update a wheel file's name (PATCH method)",
        parameters=[
            OpenApiParameter(name="id", description="ID of the wheel file", required=True, type=int)
        ],
        request={"application/json": {"type": "object", "properties": {"new_name": {"type": "string"}}}},
        responses={200: OpenApiTypes.OBJECT, 400: {"error": "Bad request"}, 404: {"error": "Not found"}},
    )
    def patch(self, request, *args, **kwargs):
        wheel_id = request.query_params.get("id")
        new_name = request.data.get("new_name")

        if not wheel_id or not new_name:
            return Response({"error": "Both ID and new_name parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            wheel = Wheel.objects.get(id=wheel_id)
            old_path = wheel.whl_file.path

            new_filename = f"{new_name}.whl"
            new_path = os.path.join(settings.MEDIA_ROOT, new_filename)

            os.rename(old_path, new_path)

            wheel.whl_file.name = new_filename
            wheel.save()

            return Response({"message": "Wheel name updated successfully.", "wheel": {"name": wheel.whl_file.name}},
                            status=status.HTTP_200_OK)

        except Wheel.DoesNotExist:
            return Response({"error": "Wheel file not found"}, status=status.HTTP_404_NOT_FOUND)
        except FileNotFoundError:
            return Response({"error": "Original file not found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        summary="Replace a wheel file",
        description="Replace an existing wheel file with a new file (PUT method)",
        parameters=[
            OpenApiParameter(name="id", description="ID of the wheel file", required=True, type=int)
        ],
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "whl_file": {
                        "type": "string",
                        "format": "binary",
                        "description": "The new .whl file to replace the existing one"
                    }
                }
            }
        },
        responses={200: OpenApiTypes.OBJECT, 400: {"error": "Bad request"}, 404: {"error": "Not found"}},
    )
    def put(self, request, *args, **kwargs):
        wheel_id = request.query_params.get("id")
        if not wheel_id:
            return Response({"error": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UploadWheelSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            wheel = Wheel.objects.get(id=wheel_id)
            wheel.whl_file = request.FILES['whl_file']
            wheel.save()
            return Response({"message": "Wheel replaced successfully.", "wheel": {"name": wheel.whl_file.name}}, status=status.HTTP_200_OK)
        except Wheel.DoesNotExist:
            return Response({"error": "Wheel file not found"}, status=status.HTTP_404_NOT_FOUND)
