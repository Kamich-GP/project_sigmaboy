from django.shortcuts import render, redirect
from .models import Category, Product, Cart
from .forms import RegForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.views import View


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


# Поиск товара по названию
def search(request):
    if request.method == 'POST':
        # Достаем данные с формы
        get_product = request.POST.get('search_product')
        # Достаем данные из БД
        searched_product = Product.objects.filter(product_name__iregex=get_product)
        if searched_product:
            context = {
                'products': searched_product,
                'request': get_product
            }
            return render(request, 'result.html', context)
        else:
            context = {
                'products': '',
                'request': get_product
            }
            return render(request, 'result.html', context)


# Регистрация
class Register(View):
    template_file = 'registration/register.html'

    def get(self, request):
        context = {'form': RegForm}
        return render(request, self.template_file, context)

    def post(self, request):
        form = RegForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password2')

            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password)
            user.save()
            login(request, user)
            return redirect('/')
