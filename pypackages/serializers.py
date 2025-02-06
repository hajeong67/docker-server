from rest_framework import serializers
from .models import Wheel

class PostWheelModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wheel
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': False},
            'version': {'required': False}
        }

    # # Object-level validation
    # def validate(self, data):
    #     if Wheel.objects.filter(name=data['name'], version=data['version']).exists():
    #         raise serializers.ValidationError("같은 이름과 버전의 Wheel이 이미 존재합니다.")
    #     return data