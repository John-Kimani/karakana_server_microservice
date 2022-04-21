from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import CustomerRegistrationform
from django.contrib.auth.decorators import login_required

def customer_register(request):
    '''
    Register customer view function
    '''
    if request.method == 'POST':
        form = CustomerRegistrationform(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(request, f'Your account has been created  you can now login')
            return redirect('customer-login')
    else:
        form = CustomerRegistrationform()
    return render(request, 'users/register.html', {"form":form})


@login_required()
def customer_profile(request):
    '''
    Customer profile view funtion
    '''

    return render(request, 'users/customer-profile.html')

