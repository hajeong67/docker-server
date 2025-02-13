from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import LoginSerializer, UserSerializer, LogoutSerializer

class LoginAPIView(APIView):
    permission_classes = [AllowAny]  # 인증 없이 가능

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=400)

            token = RefreshToken(refresh_token)
            token.blacklist()  # Refresh Token을 블랙리스트에 추가

            return Response({"message": "Successfully logged out"}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=400)

    def get(self, request):  # GET 요청이 들어오면 차단
        return Response({"error": "GET method is not allowed for logout"}, status=405)
