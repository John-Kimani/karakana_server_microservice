from django.urls import path
from .views import RegisterView, VerifyEmail, LoginAPIView, RequestPasswordResetEmail, PasswordTokenCheckAPIView, SetNewPasswordAPIView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('email/verify/', VerifyEmail.as_view(), name='email-verify'),
    path('request-reset-password/', RequestPasswordResetEmail.as_view(), name='request-password-reset'),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPIView.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-compete')
]