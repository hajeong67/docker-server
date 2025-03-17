from rest_framework import serializers

class UploadWheelSerializer(serializers.Serializer):
    whl_file = serializers.FileField()