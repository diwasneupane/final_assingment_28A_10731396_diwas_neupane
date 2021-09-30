from django import forms
from django.forms import ModelForm

from .models import Category, Food, Order

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class FoodForm(ModelForm):
    class Meta:
        model = Food
        fields = "__all__"


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['quantity', 'contact_no', 'contact_address', 'payment_method']