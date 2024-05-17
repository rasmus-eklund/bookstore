from django import template
from books.models import Cart

register = template.Library()

@register.simple_tag(takes_context=True)
def cart_book_count(context):
    request = context['request']
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return cart.get_total_quantity()