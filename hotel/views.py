from http.client import HTTPResponse
from xml.etree.ElementTree import Comment
from django.http.response import JsonResponse

from django.shortcuts import redirect, render

from .models import Cart, Category, Customer, MenuItem, OrderPlaced
from django.views import View
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import math
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView


class KhaltiView(View):
    def get(self, request, *args, **kwargs):
        o_id = request.GET.get("o_id")
        order = OrderPlaced.objects.get(id=o_id)
        context = {
            "order": order
        }
        return render(request, "khaltirequest.html", context)


class EditorChartView(TemplateView):
    template_name = 'admin/chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = MenuItem.objects.all()
        return context
# def home(request):
#     allItem = []
#     catitem = MenuItem.objects.values('category')
#     cats = {item['category'] for item in catitem}

#     for cat in cats:
#         item = MenuItem.objects.filter(category=cat)
#         n = len(item)
#         nSlides = n // 4 + math.ceil((n / 4) - (n // 4))
#         allItem.append([item, range(1, nSlides), nSlides])

#     context = {
#         'allItem': allItem,
#     }

#     return render(request, 'index.html', context)

# class EditorChartView(TemplateView):
#     template_name = 'admin/change_list.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["qs"] = MenuItem.objects.all()
#         return context


def search(request):
    query = request.GET['query']

    if query:
        allMenu = MenuItem.objects.filter(Q(name__icontains=query) |
                                          Q(price__icontains=query) |
                                          Q(description__icontains=query)
                                          )
    else:
        allMenu = MenuItem.objects.all()

    context = {
        'allMenu': allMenu
    }
    return render(request, 'hotel/search.html', context)


class ItemView(View):
    def get(self, request):

        allItem = []
        catitem = MenuItem.objects.values('category')
        cats = {item['category'] for item in catitem}

        for cat in cats:
            item = MenuItem.objects.filter(category=cat)
            n = len(item)
            nSlides = n // 4 + math.ceil((n / 4) - (n // 4))
            allItem.append([item, range(1, nSlides), nSlides])

        categories = Category.objects.all()

        context = {

            'allItem': allItem,
            'categories': categories

        }
        return render(request, 'hotel/home.html', context)

# def product_detail(request):
#     return render(request, 'app/productdetail.html')


class ItemDetailView(View):
    def get(self, request, pk):
        product = MenuItem.objects.get(id=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(
                Q(item=product.id) & Q(user=request.user)).exists()
        context = {
            'product': product,
            'item_exits': item_already_in_cart
        }
        return render(request, 'hotel/itemdetail.html', context)


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = MenuItem.objects.get(id=product_id)
    Cart(user=user, item=product).save()
    return redirect('/cart')


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)

        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        # comprehension

        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.item.price)
                amount += tempamount
                total_amount = amount + shipping_amount
        else:
            return render(request, 'hotel/emptycart.html')
        context = {
            'carts': cart,
            'total_amount': total_amount,
            'amount': amount
        }
        return render(request, 'hotel/addtocart.html', context)
    else:
        return render(request, 'hotel/emptycart.html')


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(item=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()

        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.item.price)
            amount += tempamount

        data = {

            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(item=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()

        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.item.price)
            amount += tempamount

        data = {

            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount
        }
        return JsonResponse(data)


@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(item=prod_id) & Q(user=request.user))
        c.delete()

        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.item.price)
            amount += tempamount

        data = {
            'amount': amount,
            'total_amount': amount + shipping_amount
        }
        return JsonResponse(data)


@login_required
def buy_now(request):
    return render(request, 'hotel/buynow.html')

# # def profile(request):
# #     return render(request, 'app/profile.html')


@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'hotel/address.html', {'add': add, 'active': 'btn-primary'})


@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    context = {
        'order_placed': op
    }
    return render(request, 'hotel/orders.html', context)

# # def change_password(request):
# #     return render(request, 'app/changepassword.html')


def menu(request, menu=None):

    if menu == None:
        menuitem = MenuItem.objects.all()
    else:
        menuitem = MenuItem.objects.filter(category__name=menu)

    categories = Category.objects.all()
    context = {
        'categories': categories,
        'menuitem': menuitem,

    }

    return render(request, 'hotel/menu.html', context)

# def login(request):
#     return render(request, 'app/login.html')

# # def customerregistration(request):
# #     return render(request, 'app/customerregistration.html')


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'hotel/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(
                request, 'Congratulations!! Registered successfully.')
            form.save()
        return render(request, 'hotel/customerregistration.html', {'form': form})


@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)

    item_already_in_cart = False
    if request.user.is_authenticated:
        item_already_in_cart = Customer.objects.filter(user=user).exists()

    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0

    cart_product = [p for p in Cart.objects.all() if p.user == request.user]

    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.item.price)
            amount += tempamount
        total_amount = amount + shipping_amount

    if request.method == 'POST':

        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            province = form.cleaned_data['province']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, address=address,
                           city=city, province=province, zipcode=zipcode)
            reg.save()
            messages.success(
                request, 'congratulation!! profile updadted successfully')
            return redirect('/checkout')

    else:
        form = CustomerProfileForm()

    context = {
        'item': item_already_in_cart,
        'form': form,
        'add': add,
        'total_amount': total_amount,
        'cart_items': cart_items
    }
    return render(request, 'hotel/checkout.html', context)


@login_required
def payment_done(request):

    custid = request.GET['searchquery']
    user = request.user
    customer = get_object_or_404(Customer, id=custid)

    # customer = Customer.objects.get(id=custid)

    cart = Cart.objects.filter(user=user)

    for c in cart:
        OrderPlaced(user=user, customer=customer,
                    item=c.item, quantity=c.quantity).save()
        c.delete()
    return redirect("/orders")


@method_decorator(login_required, name='dispatch')
class ProfileView(View):

    def get(self, request):

        customer = Customer.objects.filter(user=request.user)
        form = CustomerProfileForm()

        context = {
            'customer': customer,
            'form': form,
        }
        return render(request, 'hotel/profile.html', context)

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            province = form.cleaned_data['province']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, address=address,
                           city=city, province=province, zipcode=zipcode)
            reg.save()
            messages.success(
                request, 'congratulation!! profile updadted successfully')
        context = {
            'form': form,
        }
        return render(request, 'hotel/profile.html', context)
