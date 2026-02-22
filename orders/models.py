from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product
# Create your models here.

User = get_user_model()


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PROCESSING = 'PROCESSING', 'Processing'
        SHIPPED = 'SHIPPED', 'Shipped'
        DELIVERED = 'DELIVERED', 'Delivered'
        CANCELLED = 'CANCELLED', 'Cancelled'


    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # delivery Info
    full_name = models.CharField(max_length=100)
    
    phone_number = models.CharField(max_length=20)
    
    delivery_address = models.TextField()

    order_note = models.TextField(blank=True)
    # The field itself
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_paid = models.BooleanField(default=False)


    def __str__(self):
        return f"Order {self.id} by {self.full_name}"
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='order_items', null=True, blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    
    def __str__(self):
        # Added a safety check in case the product was deleted
        product_name = self.product.name if self.product else "Deleted Product"
        return f"{self.quantity}x {product_name}"
    
    def get_cost(self):
        return self.price * self.quantity