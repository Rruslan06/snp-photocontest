from rest_framework import serializers


class RegisterRequestSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(min_length=8, write_only=True)
    password_confirm = serializers.CharField(min_length=8, write_only=True)


class RegisterResponseSerializer(serializers.Serializer):
    
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField(allow_blank=True)
    access = serializers.CharField()
    refresh = serializers.CharField()