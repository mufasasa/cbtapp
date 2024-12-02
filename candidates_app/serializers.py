from rest_framework import serializers

class CandidateViewSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    nin = serializers.CharField(max_length=100, required=False, allow_null=True)
    phone = serializers.CharField(max_length=100, required=False, allow_null=True)
    phone2 = serializers.CharField(max_length=100, required=False, allow_null=True)
    photo = serializers.ImageField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)

    

class CandidateSummarySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    created_at = serializers.DateTimeField(read_only=True)
    photo = serializers.ImageField(required=False, allow_null=True)
