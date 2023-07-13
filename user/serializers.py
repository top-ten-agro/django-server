from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser


class UserSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'password', 'email',
                  'name',   'phone')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.phone = validated_data.get('phone', instance.phone)
        password = validated_data.get('password', None)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['name'] = user.name
        return token
