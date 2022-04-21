from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import CustomerRegistrationform

def customer_register(request):
    '''
    Register customer view function
    '''
    if request.method == 'POST':
        form = CustomerRegistrationform(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(request, f'Account created for {username}!')
            return redirect('HomePage')
    else:
        form = CustomerRegistrationform()
    return render(request, 'users/register.html', {"form":form})

