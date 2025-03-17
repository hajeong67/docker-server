from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from rest_framework import serializers

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(help_text="The refresh token to blacklist")

@extend_schema(tags=["users"])
class LogoutAPIView(APIView):
    @extend_schema(
        summary="User Logout",
        description="Logs out a user by blacklisting the refresh token.",
        request=LogoutSerializer,
        responses={205: None, 400: {"error": "Bad request"}, 401: {"error": "Invalid token"}},
    )
    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # refresh_token을 블랙리스트에 추가
        except Exception as e:
            return Response({"error": f"Invalid refresh token: {str(e)}"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
