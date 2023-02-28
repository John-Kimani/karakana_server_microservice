from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

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
    def get(self):
        pass