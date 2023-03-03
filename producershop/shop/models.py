from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from uuid import uuid4


class ContactRequest(models.Model):
    email = models.EmailField()
    content = models.TextField()
    real_contact = models.BooleanField()
    done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Genre(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=50)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT)
    file = models.FileField(upload_to='shop/audio')
    tagged_file = models.FileField(
        upload_to='shop/audio', null=True, blank=True)
    cover_img = models.FileField(upload_to='shop/images')
    price = models.DecimalField(
        decimal_places=2, max_digits=6, validators=[MinValueValidator(0)])
    avaiable = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
