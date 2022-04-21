from django.urls import path
from . import views


urlpatterns = [

    path('', views.index, name='HomePage'),
    path('about-us/', views.about_us, name='AboutUs'),
    path('contact-us/', views.contact_us, name='ContactUs')
]