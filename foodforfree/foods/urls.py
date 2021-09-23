from django.urls import path
from . import views
urlpatterns = [
    path('category_form', views.category_form),
    path('get_category', views.get_category),
    path('delete_category/<int:category_id>', views.delete_category),
]
