from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid username or password.")

        data['user'] = user
        return data

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        refresh_token = data.get("refresh")

        # refresh_token이 누락되거나 빈 값인 경우 처리
        if not refresh_token:
            raise serializers.ValidationError({"refresh": "This field is required and cannot be blank."})

        try:
            # Refresh Token 유효성 검증
            RefreshToken(refresh_token)
        except Exception as e:
            raise serializers.ValidationError({"refresh": "Invalid refresh token. Error: " + str(e)})

        return data