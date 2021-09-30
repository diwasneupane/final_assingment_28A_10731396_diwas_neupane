from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve
from .views import homepage, delete_category, category_form
from .models import Category, Food


class TestUrls(SimpleTestCase):
    def test_about(self):
        url = reverse('homepage')
        self.assertEquals(resolve(url).func, homepage)

    def test_delete_contact_url(self):
        url = reverse('delete_category', args=[1])
        self.assertEquals(resolve(url).func, delete_category)

    def test_get_FAQ_url(self):
        url = reverse('category_form')
        self.assertEquals(resolve(url).func, category_form)


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_news_url = reverse('menu')
        self.contact_form_url = reverse('show_categories')

    def test_home_news(self):
        response = self.client.get(self.home_news_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'foods/menu.html')

    def test_contact_form(self):
        response = self.client.get(self.contact_form_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'foods/show_categories.html')


class TestModels(TestCase):
    def setUp(self):
        self.Category = Category.objects.create(
            category_name='Diwas',
            category_description="Math"
        )
        self.Food = Food.objects.create(
            food_name='Diwas',
            food_price="123",
        )

    def test_food_menu_model(self):
        self.assertEquals(self.Category.category_name, 'Diwas')

    def test_food_category_model(self):
        self.assertEquals(self.Food.food_name, 'Diwas')
