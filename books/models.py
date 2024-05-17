from django.db import models
from django.contrib.auth.models import User
from books.utils import toSek

# Create your models here.

class Book(models.Model):
  title = models.CharField(max_length=200)
  author = models.CharField(max_length=200)
  description = models.TextField()
  price = models.DecimalField(max_digits=10, decimal_places=2)
  publication_date = models.DateField()
  cover_image = models.URLField()

  def __str__(self) -> str:
    return f'{self.author}: {self.title}'

  def get_price(self) -> str:
     return toSek(self.price)

  
class CartItem(models.Model):
   book = models.OneToOneField(Book, on_delete=models.CASCADE)
   quantity = models.IntegerField(default=1)

   def __str__(self) -> str:
      return f'{self.book} | {self.quantity} st'

   def price(self) -> str:
      return self.book.price * self.quantity
   
   def get_price(self):
      return toSek(self.price())

   def increment(self):
      self.quantity += 1
      self.save(update_fields=["quantity"])
   
   def decrement(self):
      self.quantity -= 1
      self.save(update_fields=["quantity"])

class Cart(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  items = models.ManyToManyField(CartItem, blank=True)
  
  def total_price(self):
    return toSek(sum(item.price() for item in self.items.all()))

  def get_total_quantity(self):
     items = self.items.all()
     return sum(item.quantity for item in items)
  
  def __str__(self) -> str:
    return self.user.username
