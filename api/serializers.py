from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import make_password
from product.models import Product, Category



class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')
        extra_kwargs = {"password":{'write_only': True}}



    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = super().create(validated_data)
        refresh = RefreshToken.for_user(user)

        # Add the JWT tokens to the response
        validated_data['refresh'] = str(refresh)
        validated_data['access'] = str(refresh.access_token)

        return validated_data




class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="Enter your username", label="Username")
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        help_text="Enter your password",
        label="Password"
    )


    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        # Authenticate user
        user = authenticate(request=self.context.get('request'), username=username, password=password)

        if not user:
            raise serializers.ValidationError('Invalid credentials')

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        attrs['tokens'] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return attrs

class ProductSerializer(serializers.ModelSerializer):
    # image = serializers.ImageField(max_length=None, allow_empty_file=True, allow_null=True)
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Add JWT token to the representation
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            token = AccessToken.for_user(request.user)
            representation['token'] = str(token)

        return representation