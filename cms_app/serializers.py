import django.contrib.auth.password_validation as validators
from rest_framework import serializers
from .models import UserRegister, ContentItem


class UserRegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserRegister
        fields = ('id', 'email', 'full_name', 'phone', 'password', 'pincode')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, data):
        min_length=1
        
        # print(data)
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if len(data) < 8:
            raise serializers.ValidationError(('Password must contain at least 8 letters'))
        if not any(char.isdigit() for char in data):
            raise serializers.ValidationError(('Password must contain at least %(min_length)d digit.') % {'min_length': min_length})
        if not any(char.isalpha() for char in data):
            raise serializers.ValidationError(('Password must contain at least %(min_length)d letter.') % {'min_length': min_length})
        if not any(char in special_characters for char in data):
            raise serializers.ValidationError(('Password must contain at least %(min_length)d special character.') % {'min_length': min_length})
        return data

    def save(self):
        data = UserRegister(
            email=self.validated_data['email'],
            full_name=self.validated_data['full_name'],
            phone=self.validated_data['phone'],
            pincode=self.validated_data['pincode'],
        )
        password=self.validated_data['password']
        data.set_password(password)
        data.save()
        return data


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True, required=True
    )

    class Meta:
        model = UserRegister
        fields = (
            'email',
            'password'
        )


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentItem
        fields = ('id', 'user', 'title', 'body', 'summary', 'document', 'category')
        extra_kwargs = {'user': {'read_only': True}}