from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Book, Cart, CartItem

# Create your views here.

def book_list(request):
  books = Book.objects.all()
  return render(request, 'books/book_list.html', {'books': books})

def book_details(request, book_id):
  book = get_object_or_404(Book, pk=book_id)
  return render(request, 'books/book.html', {'book': book})

def search_books(request):
    keyword = request.GET.get('q')
    books = Book.objects.filter(Q(title__icontains=keyword) | Q(author__icontains=keyword) | Q(
            description__icontains=keyword))
    return render(request, 'books/book_list.html', {'books': books, 'query': keyword})


@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    if cart.items.filter(book=book).exists():
        item = cart.items.get(book=book)
        item.increment()
    else:
        item, _ = CartItem.objects.get_or_create(book=book)
        cart.items.add(item)
    return HttpResponseRedirect(reverse('books'))

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return HttpResponseRedirect(reverse('cart_detail'))

@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total = cart.total_price()
    return render(request, 'books/cart_detail.html', {'items': items, 'total': total})

@login_required
def increment_item(request, item_id):
  item = get_object_or_404(CartItem, id=item_id)
  item.increment()
  return HttpResponseRedirect(reverse('cart_detail'))

@login_required
def decrement_item(request, item_id):
  item = get_object_or_404(CartItem, id=item_id)
  if item.quantity == 1:
     item.delete()
  else:
    item.decrement()
  return HttpResponseRedirect(reverse('cart_detail'))

   
   