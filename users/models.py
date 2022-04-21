from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils import timezone


class CustomerProfile(models.Model):
    '''
    Class that handles customer profile
    '''
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_profile_picture = CloudinaryField('karakana/assets/', default='https://res.cloudinary.com/dbgbail9r/image/upload/v1650578825/karakana/user-authentication/user_profile_image.jpg')
    customer_bio = models.TextField(max_length=50, blank=True)
    customer_phone_number = models.CharField(max_length=17, blank=True, null=True)
    customer_location = models.CharField(max_length=25, blank=True, null=True)
    customer_since = models.DateField(default=timezone.now)

    def __str__(self):
        return self.customer_bio