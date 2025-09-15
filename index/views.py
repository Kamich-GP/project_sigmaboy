from django.shortcuts import render, redirect
from .models import Category, Product, Cart
from .forms import RegForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.views import View
import telebot

bot = telebot.TeleBot('TOKEN')
group_id = "GROUP_ID"

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


# Выход из аккаунта
def logout_view(request):
    logout(request)
    return redirect('/')


# Добавление товара в корзину
def add_to_cart(request, pk):
    if request.method == 'POST':
        product = Product.objects.get(id=pk)
        user_count = int(request.POST.get('pr_amount'))
        if 1 <= user_count <= product.product_count:
            Cart.objects.create(user_id=request.user.id,
                                user_product=product,
                                user_pr_amount=user_count).save()
            return redirect('/')
        return redirect(f'/product/{pk}')


# Удаление товара из корзины
def del_from_cart(request, pk):
    Cart.objects.filter(user_product=Product.objects.get(id=pk)).delete()
    return redirect('/cart')


# Отображение корзины
def cart(request):
    user_cart = Cart.objects.filter(user_id=request.user.id)
    totals = [round(t.user_product.product_price * t.user_pr_amount) for t in user_cart]
    context = {
        'cart': user_cart,
        'total': round(sum(totals))
    }

    if request.method == 'POST':
        text = (f'Новый заказ!\n'
                f'Клиент: {User.objects.get(id=request.user.id).email}\n\n')

        for i in user_cart:
            product = Product.objects.get(id=i.user_product.id)
            product.product_count = product.product_count - i.user_pr_amount
            product.save(update_fields=['product_count'])

            text += (f'Товар: {i.user_product}\n'
                     f'Количество: {i.user_pr_amount}\n'
                     f'--------------------------------\n')
        text += f'Итого: ${round(sum(totals))}'
        bot.send_message(group_id, text)
        user_cart.delete()
        return redirect('/')

    return render(request, 'cart.html', context)
