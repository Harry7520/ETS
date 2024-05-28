from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class serviceCategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(default=None, blank=True)

    def __str__(self):
        return self.name
    
class Service(models.Model):
    category = models.ForeignKey(serviceCategory, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    description = models.TextField(default=None)
    create_at = models.DateTimeField(default=None)
    image = models.ImageField(default=None,blank=True)

    def __str__(self):
        return self.name

class Gender(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Occupation(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    image = models.ImageField(default=None, blank=True)
    password = models.CharField(max_length=30)
    create_at = models.DateTimeField(default=None)

    def __str__(self):
        return self.name

class Technician(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    birth = models.DateField()
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, default=None)
    nrc = models.CharField(max_length=100)
    image = models.ImageField(default=None, blank=True)
    occupation = models.ForeignKey(Occupation, on_delete=models.CASCADE, default=None)
    qualification = models.TextField()
    password = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    create_at = models.DateTimeField(default=None)

    def __str__(self):
        return self.full_name

class M_Occupation(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Main(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    image = models.ImageField(default=None, blank=True)
    occupation = models.ForeignKey(M_Occupation, on_delete=models.CASCADE, default=None)
    password = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    create_at = models.DateTimeField(default=None)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    service = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    c_name = models.CharField(max_length=50)
    t_name = models.CharField(max_length=50)
    c_email = models.EmailField()
    t_email = models.EmailField()
    t_phone = models.CharField(max_length=20)
    c_phone = models.CharField(max_length=20)
    c_address = models.CharField(max_length=100)
    order_date = models.DateField()
    status = models.CharField(max_length=12,default='pending')
    f_status = models.CharField(max_length=12,default='pending')
    t_status = models.BooleanField(default=True)
    c_status = models.BooleanField(default=True)
    create_at = models.DateTimeField(default=None)

    def __str__(self):
        return self.service
    
class Review(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    message = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    create_at = models.DateTimeField(default=None)

    def __str__(self):
        return self.name