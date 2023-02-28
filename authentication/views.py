from django.shortcuts import render
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)

        if serializer.is_valid(raise_exception=True):
        
            serializer.save()

            user_data = serializer.data

            user = User.objects.get(email=user_data['email'])

            # Get users access token
            token = RefreshToken.for_user(user).access_token
            
            # Get current site domain
            current_site = get_current_site(request).domain

            # Pass to the correct system endpoint
            relativeLink = reverse('email-verify')

            # Redirected site link
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

            return Response(data=user_data, status=status.HTTP_201_CREATED)
        

class VerifyEmail(views.APIView):

    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):

        token = request.GET.get('token')

        print(token)

        try:
            ## When using pwt > version 2 provide algoriths to decode tokens
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

            print(payload)

            user = User.objects.get(id=payload['user_id'])

            print(user)

            if not user.is_verified:

                user.is_verified = True

                user.save()

            response = {
                'email': 'Account sucessfully activated'
            }

            return Response(response, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            response = {
                'error': 'Activation link expired'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            response = {
                'error': 'Invalid token'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        

class LoginAPIView(generics.GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)

        if serializer.is_valid(raise_exception=True):

            response = {
                'message': 'Login Sucess',
                'user': serializer.data
            }

            return Response(data=response, status=status.HTTP_200_OK)
