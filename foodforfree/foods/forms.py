from django import forms
from django.forms import ModelForm
from .models import Category, Food

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class FoodForm(ModelForm):
    class Meta:
        model = Food
        fields = "__all__"