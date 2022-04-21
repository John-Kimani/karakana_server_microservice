from django.shortcuts import render

def product_list(request):
    '''
    Main/homepage view function
    '''
    return render(request, 'products/products.html')

def add_to_cart(request):
    '''
    About us view function
    '''
    return render(request, 'products/cart.html')


def checkout(request):
    '''
    Contact us view function
    '''
    return render(request, 'products/checkout.html')
