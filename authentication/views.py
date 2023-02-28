from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings

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
        

class VerifyEmail(generics.GenericAPIView):
    def get(self, request):

        token = request.GET.get('token')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)

            user = User.objects.get(id=payload['user_id'])

            if not user.is_verified:

                user.is_verified = True

                user.save()

            response = {
                'email': 'Account sucessfully activated'
            }

            return Response(response, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            response = {
                'error': 'Activation link expired'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            response = {
                'error': 'Invalid token'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)