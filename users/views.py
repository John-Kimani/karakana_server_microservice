from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def register(request):
    '''
    Register users view function
    '''
    form = UserCreationForm()
    return render(request, 'users/register.html', {"form":form})

