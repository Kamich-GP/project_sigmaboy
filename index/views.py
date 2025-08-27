from django.shortcuts import render
from .models import Category, Product, Cart


# Create your views here.
def home_page(request):
    # Достаем все из БД
    categories = Category.objects.all()
    products = Product.objects.all()
    # Передаем данные на Frontend
    context = {
        'categories': categories,
        'products': products
    }
    return render(request, 'home.html', context)
