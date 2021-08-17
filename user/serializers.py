from django.core import exceptions
from rest_framework import serializers
import django.contrib.auth.password_validation as validators
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'middle_name',
                  'last_name', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        user = User(**data)
        password = data.get('password')
        error = dict()
        try:
            validators.validate_password(password=password, user=User)
        except exceptions.ValidationError as e:
            error['password'] = list(e.messages)

        if error:
            raise serializers.ValidationError(error)

        return super(UserRegistrationSerializer, self).validate(data)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name',
                  'middle_name', 'last_name', 'role']
        extra_kwargs = {'id': {'read_only': True}}
