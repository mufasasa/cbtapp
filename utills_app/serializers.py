from rest_framework import serializers



class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def create(self, validated_data):
        return validated_data['file']