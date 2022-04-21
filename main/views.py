from django.shortcuts import render

def index(request):
    '''
    Main/homepage view function
    '''
    return render(request, 'main/main.html')

def about_us(request):
    '''
    About us view function
    '''
    return render(request, 'main/about.html')


def contact_us(request):
    '''
    Contact us view function
    '''
    return render(request, 'main/contacts.html')
