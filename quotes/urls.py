from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('portfolio', views.portfolio, name="portfolio"),
    path('about', views.about, name="about"),
    path('add_stock/', views.add_stock, name="add_stock"),
    path('applog/', views.applog, name="applog"),
    path('delete_stock/<stock_id>', views.delete_stock, name="delete_stock"),
]