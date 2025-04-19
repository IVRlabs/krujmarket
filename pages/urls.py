from django.urls import path
from .views import AboutView, ContactsView, BlogView, DostavkaView

from .views import HomeView

app_name = 'pages'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # Главная страница
    path('about/', AboutView.as_view(), name='about'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('dostavka_oplata/', DostavkaView.as_view(), name='dostavka_oplata')
]