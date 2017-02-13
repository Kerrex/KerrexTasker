from rest_framework import serializers

from taskbackend.models import Project


class AuthSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    login = serializers.CharField()
    password = serializers.CharField()


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
