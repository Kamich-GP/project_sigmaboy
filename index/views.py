from django.shortcuts import render
from .models import Category, Product, Cart


# Create your views here.
# Главная страница
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


# Страница выбранной категории
def category_page(request, pk):
    # Достаем данные из БД
    category = Category.objects.get(id=pk)
    products = Product.objects.filter(product_category=category)
    # Передаем данные на Frontend
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'category.html', context)


# Страница выбранного товара
def product_page(request, pk):
    # Достаем данные из БД
    product = Product.objects.get(id=pk)
    # Передаем данные на Frontend
    context = {'product': product}
    return render(request, 'product.html', context)
