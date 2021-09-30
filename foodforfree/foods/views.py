from django.shortcuts import render, redirect
from .forms import CategoryForm, FoodForm, OrderForm
from django.contrib import messages
from .models import Category, Food, Cart, Order

from accounts.auth import admin_only, user_only
from django.contrib.auth.decorators import login_required
import os


def homepage(request):
    return render(request, 'foods/homepage.html')


@login_required
@admin_only
def category_form(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Category added successfully')
            return redirect("/foods/get_category")
        else:
            messages.add_message(request, messages.ERROR, 'Unable to add category')
            return render(request, 'foods/category_form.html', {'form_category':form})
    context ={
        'form_category': CategoryForm,
        'activate_category': 'active'
    }
    return render(request, 'foods/category_form.html', context)

@login_required
@admin_only
def get_category(request):
    categories =  Category.objects.all().order_by('-id')
    context = {
        'categories':categories,
        'activate_category':'active'
    }
    return render(request, 'foods/get_category.html', context)


@login_required
@admin_only
def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    messages.add_message(request, messages.SUCCESS, 'Category Deleted Successfully')
    return redirect('/foods/get_category')



@login_required
@admin_only
def category_update_form(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == "POST":
        form = CategoryForm(request.POST,instance=category)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Category updated successfully')
            return redirect("/foods/get_category")
        else:
            messages.add_message(request, messages.ERROR, 'Unable to update category')
            return render(request, 'foods/category_update_form.html', {'form_category':form})
    context ={
        'form_category': CategoryForm(instance=category),
        'activate_category': 'active'
    }
    return render(request, 'foods/category_update_form.html', context)

@login_required
@admin_only
def food_form(request):
    if request.method == "POST":
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Food added successfully')
            return redirect("/foods/get_food")
        else:
            messages.add_message(request, messages.ERROR, 'Unable to add food')
            return render(request, 'foods/food_form.html', {'form_food':form})
    context ={
        'form_food': FoodForm,
        'activate_food': 'active'
    }
    return render(request, 'foods/food_form.html', context)


@login_required
@admin_only
def get_food(request):
    foods =  Food.objects.all().order_by('-id')
    context = {
        'foods':foods,
        'activate_food':'active'
    }
    return render(request, 'foods/get_food.html', context)


@login_required
@admin_only
def delete_food(request, food_id):
    food = Food.objects.get(id=food_id)
    os.remove(food.food_image.path)
    food.delete()
    messages.add_message(request, messages.SUCCESS, 'Food Deleted Successfully')
    return redirect('/foods/get_food')


@login_required
@admin_only
def food_update_form(request, food_id):
    food = Food.objects.get(id=food_id)
    if request.method == "POST":
        if request.FILES.get('food_image'):
            os.remove(food.food_image.path)
        form = FoodForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Food updated successfully')
            return redirect("/foods/get_food")
        else:
            messages.add_message(request, messages.ERROR, 'Unable to update food')
            return render(request, 'foods/food_form.html', {'form_food':form})
    context ={
        'form_food': FoodForm(instance=food),
        'activate_food': 'active'
    }
    return render(request, 'foods/food_update_form.html', context)


def show_categories(request):
    categories = Category.objects.all().order_by('-id')
    context = {
        'categories':categories,
        'activate_category_user': 'active'
    }
    return render(request, 'foods/show_categories.html', context)


def show_foods(request):
    foods = Food.objects.all().order_by('-id')
    context = {
        'foods':foods,
        'activate_food_user': 'active'
    }
    return render(request, 'foods/show_foods.html', context)

def menu(request):
    categories  = Category.objects.all().order_by('-id')
    context = {
        'categories':categories,
        'activate_menu':'active'
    }
    return render(request, 'foods/menu.html', context)

@login_required
@user_only
def add_to_cart(request, food_id):
    user = request.user
    food = Food.objects.get(id=food_id)

    check_item_presence = Cart.objects.filter(user=user, food=food)
    if check_item_presence:
        messages.add_message(request, messages.ERROR, 'Item is already present in cart')
        return redirect('/foods/get_food_user')
    else:
        cart = Cart.objects.create(food=food, user=user)
        if cart:
            messages.add_message(request, messages.SUCCESS, 'Item added to cart')
            return redirect('/foods/mycart')
        else:
            messages.add_message(request, messages.ERROR, 'Unable to add item to cart')


@login_required
@user_only
def show_cart_items(request):
    user = request.user
    items = Cart.objects.filter(user= user)
    context = {
        'items':items,
        'activate_my_cart':'active'
    }
    return render(request, 'foods/mycart.html', context)

@login_required
@user_only
def remove_cart_item(request, cart_id):
    item = Cart.objects.get(id=cart_id)
    item.delete()
    messages.add_message(request, messages.SUCCESS, 'Cart item removed successfully')
    return redirect('/foods/mycart')


@login_required
@user_only
def order_form(request, food_id,cart_id):
    user = request.user
    food = Food.objects.get(id=food_id)
    cart_item = Cart.objects.get(id=cart_id)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            quantity = request.POST.get('quantity')
            price = food.food_price
            total_price = int(quantity)*int(price)
            contact_no = request.POST.get('contact_no')
            contact_address = request.POST.get('contact_address')
            payment_method = request.POST.get('payment_method')
            order = Order.objects.create(food=food,
                                         user =user,
                                         quantity=quantity,
                                         total_price=total_price,
                                         contact_no = contact_no,
                                         contact_address =contact_address,
                                         status="Pending",
                                         payment_method= payment_method,
                                         payment_status=False
            )
            if order:
                # messages.add_message(request, messages.SUCCESS, 'Item Ordered. Continue Payment for Verification')
                # cart_item.delete()
                context = {
                    'order':order,
                    'cart':cart_item
                }
                return render(request, 'foods/esewa_payment.html', context)
        else:
            messages.add_message(request, messages.ERROR, 'Something went wrong')
            return render(request, 'foods/order_form.html', {'order_form':form})
    context = {
        'order_form': OrderForm
    }
    return render(request, 'foods/order_form.html', context)


import request as req
def esewa_verify(request):
    import xml.etree.ElementTree as ET
    o_id = request.GET.get('oid')
    amount = request.GET.get('amt')
    refId = request.GET.get('refId')
    url = "https://uat.esewa.com.np/epay/transrec"
    d = {
        'amt': amount,
        'scd': 'EPAYTEST',
        'rid': refId,
        'pid': o_id,
    }
    resp = req.post(url, d)
    root = ET.fromstring(resp.content)
    status = root[0].text.strip()
    if status == 'Success':
        order_id = o_id.split("_")[0]
        order = Order.objects.get(id=order_id)
        order.payment_status = True
        order.save()
        cart_id = o_id.split("_")[1]
        cart = Cart.objects.get(id=cart_id)
        cart.delete()
        messages.add_message(request, messages.SUCCESS, 'Payment Successful')
        return redirect('/foods/mycart')
    else:
        messages.add_message(request, messages.ERROR, 'Unable to make payment')
        return redirect('/foods/mycart')


@login_required
@user_only
def my_order(request):
    user = request.user
    items = Order.objects.filter(user=user).order_by('-id')
    context = {
        'items':items,
        'activate_myorders':'active'
    }
    return render(request, 'foods/my_order.html', context)