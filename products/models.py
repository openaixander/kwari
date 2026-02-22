from django.db import models
from autoslug import AutoSlugField
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True)

    icon_class = models.CharField(max_length=50, blank=True)


    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
    

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True)
    image = models.ImageField(upload_to='products/')
    description = models.TextField(blank=True)


    price = models.DecimalField(max_digits=10, decimal_places=2)


    # stock management
    stock = models.PositiveIntegerField(default=0)

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

    @property
    def is_in_stock(self):
        return self.stock > 0




    