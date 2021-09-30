from django.shortcuts import render, redirect
from .forms import CategoryForm, FoodForm
from django.contrib import messages
from .models import Category, Food


def homepage(request):
    return render(request, 'foods/homepage.html')


# Create your views here.

def category_form(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Category added successfully')
            return redirect("/foods/get_category")
        else:
            messages.add_message(request, messages.ERROR, 'unable to add category')
            return render(request, 'foods/category_form.html', {'form_category': format()})
    context = {
        'form_category': CategoryForm,
        'activate_category': 'active'
    }

    return render(request, 'foods/category_form.html', context)


def get_category(request):
    categories = Category.objects.all().order_by('-id')
    context = {
        'categories': categories,
        'activate_category': 'active'
    }
    return render(request, 'foods/get_category.html', context)


def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    messages.add_message(request, messages.SUCCESS, 'Category Deleted Successfully')
    return redirect('/foods/get_category')
