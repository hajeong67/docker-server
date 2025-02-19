from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        refresh_token = data.get("refresh")

        if not refresh_token:
            raise serializers.ValidationError({"refresh": "This field is required and cannot be blank."})

        try:
            RefreshToken(refresh_token)
        except Exception as e:
            raise serializers.ValidationError({"refresh": "Invalid refresh token. Error: " + str(e)})

        return data