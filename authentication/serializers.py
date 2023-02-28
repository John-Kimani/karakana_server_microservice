from rest_framework import serializers
from .models import User
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']


    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError('The username should contain alphanumeric characters')
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class EmailVerificationSerializer(serializers.ModelField):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=84, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(read_only=True)
    tokens = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')

        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }
        
class RequestPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=3)

    class Meta:
        fields = ['email']

    def validate(self, attrs):

        try:
            email = attrs['data'].get('email', '')

            if User.objects.filter(email=email).exists():
                user = User.objects.filter(email=email)
                uidb64 = urlsafe_base64_encode(user.id)
                token = PasswordResetTokenGenerator().make_token(user=user)
                current_site = get_current_site(request = attrs['data'].get('request')).domain
                relativeLink = reverse('email-verify')
                absurl = 'http://'+current_site+relativeLink+'?token='+str(token)
                
                email_body = f'Hello {user.username} use the link below to verify your email address to activate your account \
                    {absurl}'

                data = {
                    'email_body': email_body,
                    'to_email': user.email,
                    'email_subject': 'Verify your email address',
                }

                ## Marked as a static method to allow direct injection
                Util.send_email(data=data)
            return attrs
        except:
            pass
        return super().validate(attrs)