from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site

class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)

        if serializer.is_valid(raise_exception=True):
        
            serializer.save()

            user_data = serializer.data

            user = User.objects.get(email=user_data['email'])

            token = RefreshToken.for_user(user)

            current_site = get_current_site(request)

            relativeLink=''

            data = {
                'domain': current_site.domain,

            }

            ## Marked as a static method to allow direct injection
            Util.send_email(data=data)

            return Response(data=user_data, status=status.HTTP_201_CREATED)
        

class VerifyEmail(generics.GenericAPIView):
    def get(self):
        pass