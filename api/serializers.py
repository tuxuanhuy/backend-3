from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import *

class FaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Face
        fields = ['picture']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'get_full_name', 
            'email', 
            'contact', 
            'address', 
            # 'picture', 
            'username',
            'password'
        ]


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = [
            'id', 
            'name', 
            'start_time', 
            'end_time', 
            'date',
            'status',
            'user'
        ]


class LoginSerializer(serializers.Serializer):
    # model = User
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True)


# Serializer to Register User
class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, 
        validators=[validate_password])

    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'password2',
                   'contact', 'address')
        extra_kwargs = {
            'full_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            first_name   = validated_data['first_name'],
            last_name    = validated_data['last_name'],
            username     = validated_data['username'],
            email        = validated_data['email'],
            address      = validated_data['address'],
            contact      = validated_data['contact'],
            # picture      = validated_data['picture'],
        )
        
        user.set_password(validated_data['password'])
        user.save()

        return user