from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.book_list, name='books'),
    url(r'^(\d+)/$', views.book_details, name='book'),
    url(r'^cart/add/(\d+)/$', views.add_to_cart, name='add_to_cart'),
    url(r'^cart/remove/(\d+)/$', views.remove_from_cart, name='remove_from_cart'),
    url(r'^cart/increment/(\d+)/$', views.increment_item, name='increment'),
    url(r'^cart/decrement/(\d+)/$', views.decrement_item, name='decrement'),
    url(r'^search/', views.search_books, name='search_books'),
    url(r'^cart/$', views.cart_detail, name='cart_detail'),
]