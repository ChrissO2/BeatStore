from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class ContactRequest(models.Model):
    email = models.EmailField()
    content = models.TextField()
    real_contact = models.BooleanField()
    done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)


class Category(models.Model):
    name = models.CharField(max_length=100)


class Sample(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    file = models.FileField()
    tagged_file = models.FileField(null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)


class Order(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    full_price = models.DecimalField(decimal_places=2, max_digits=10)


class SampleOrder(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    price = models.DecimalField(decimal_places=2, max_digits=10)
