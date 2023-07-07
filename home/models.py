from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    logo = models.CharField(max_length=300, blank=True)
    slug = models.CharField(max_length=500, unique= True)

    def __str__(self):
        return self.name
    
class Slider(models.Model):
    name = models.CharField(max_length=500)
    image = models.ImageField(upload_to='media')
    description = models.TextField(blank= True)
    rank = models.IntegerField()
    url = models.URLField(blank=True, max_length=600)

    def __str__(self):
        return self.name
    
class Ad(models.Model):
    name = models.CharField(max_length=500)
    image = models.ImageField(upload_to='media')
    description = models.TextField(blank= True)
    rank = models.IntegerField()

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=500)
    image = models.ImageField(upload_to='media')
    rank = models.IntegerField()
    slug = models.CharField(max_length=500, default = "")

    def __str__(self):
        return self.name
    
class Review(models.Model):
    customer_name = models.CharField(max_length=500)
    image = models.ImageField(upload_to='media')
    job = models.CharField(max_length=500)
    comment = models.TextField()
    rank = models.IntegerField()

    def __str__(self):
        return self.customer_name

STOCK = (('in_stock', 'In Stock'), ('out_of_stock','Out Of Stock'))
LABELS = (('', 'default'), ('new', 'new'), ('sale', 'sale'), ('hot', 'hot'))
    
class Product(models.Model):
    name = models.CharField(max_length=500)
    image = models.ImageField(upload_to='media')
    price = models.FloatField()
    discounted_price = models.FloatField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    description = models.TextField(blank= True)
    spacification = models.TextField(blank= True)
    stock = models.CharField(choices=STOCK, max_length=50)
    labels = models.CharField(choices=LABELS, max_length=50, blank=True)
    slug = models.CharField(max_length=500, default = "")

    def __str__(self):
        return self.name
    
