from django.views.generic import TemplateView
from products.models import Product  # Импортируем модель товаров


class AboutView(TemplateView):
    template_name = 'pages/about.html'  # Путь к шаблону

class ContactsView(TemplateView):
    template_name = 'pages/contacts.html'

class BlogView(TemplateView):
    template_name = 'pages/blog.html'


class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_products'] = Product.objects.filter(is_featured=True)[:3]
        return context