import decimal
import json

from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.conf.global_settings import EMAIL_HOST

from .forms import forms
from .models import *
from producershop.private_data import PRODUCER_MAIL


def index(request):
    return render(request, 'shop/base.html')


class ContactFormView(View):
    form_class = forms.ContactForm
    template_name = 'shop/contact.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        ctx = {
            'form': form,
        }
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        form = forms.ContactForm(request.POST)
        ctx = {
            'form': form,
            'msg': 'Something went wrong, try again.'
        }
        if form.is_valid():
            ctx['msg'] = 'Request send succesfully.'
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']
            content += f"\n\nSender email: {email}"
            live_contact = form.cleaned_data['live_contact']
            if live_contact:
                content += f"\nLive contact: Yes"
            else:
                content += f"\nLive contact: No"
            user = None
            try:
                user = User.objects.get(email=email)
            except ObjectDoesNotExist:
                pass
            contact_request = ContactRequest(
                email=email,
                content=content,
                real_contact=live_contact,
            )
            if user:
                contact_request.user = user

            contact_request.save()

            send_mail(subject=f"Contact Request {contact_request.pk}",
                      message=content, from_email=email, recipient_list=[PRODUCER_MAIL, EMAIL_HOST])
            return render(request, self.template_name, ctx)
        return render(request, self.template_name, ctx)


class ProductsView(View):
    template_name = 'shop/products.html'

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(avaiable=True)
        user = request.user
        ctx = {
            "products": products,
            'user': user
        }
        return render(request, self.template_name, ctx)


def cart_view(request):
    template_name = 'shop/cart.html'
    user = request.user
    order, created = Order.objects.get_or_create(user=user, complete=False)
    order_items = OrderItem.objects.filter(order=order)
    total_price = decimal.Decimal(0.00)
    for item in order_items:
        total_price += item.product.price
    ctx = {
        'order_items': order_items,
        'order': order,
        'user': user,
        'total_price': total_price,
        'created': created
    }
    return render(request, template_name, ctx)


def about_me_view(request, *args, **kwargs):
    return render(request, 'shop/about_me.html')


def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']

    user = request.user
    product = Product.objects.get(id=product_id)

    order, created_order = Order.objects.get_or_create(
        user=user, complete=False)

    order_item, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add' and not order_item:
        order_item.save()
        return JsonResponse('Item was added', safe=False)
    elif action == 'remove' and order_item:
        order_item.delete()
        return JsonResponse('Item was removed', safe=False)
    else:
        return JsonResponse('Nothing happened', safe=False)


def register_view(request):
    form = forms.CreateUserForm
    ctx = {'form': form}

    if request.method == 'POST':
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account has been created')
            return redirect('login')
        else:
            ctx['error'] = 'Something went wrong try again!'

    return render(request, 'shop/register.html', ctx)


class LoginFormView(View):
    template = 'shop/login.html'
    form = AuthenticationForm
    ctx = {'form': form}

    def get(self, request):
        return render(request, self.template, self.ctx)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('products')

        self.ctx['error'] = 'Your credidentails do not much any account. Try again.'

        return render(request, self.template, self.ctx)


def log_out_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('products')
