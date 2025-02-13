from rest_framework import serializers
from .models import Wheel
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

@extend_schema_serializer(
    exclude_fields=['description'],  # 'description' 필드를 스키마에서 제외
    examples=[
        OpenApiExample(
            "Wheel Example",
            summary="A sample wheel upload",
            description="An example of uploading a wheel file.",
            value={
                "name": "example_wheel",
                "version": "1.0.0",
                "whl_file": "path/to/file.whl",
                "author": 1,
                "summary": "This is an example wheel.",
                "license": "MIT",
                "keywords": "example, wheel",
            },
        ),
    ],
)
class PostWheelModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wheel
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': False},
            'version': {'required': False},
        }