from django.contrib import admin
from .models import Order, OrderItem

# This allows us to see the OrderItems INSIDE the Order admin page
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    # We use raw_id_fields so we don't load a massive dropdown of 10,000 products
    raw_id_fields = ['product'] 
    extra = 0 # Don't show extra empty rows

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'phone_number', 'status', 'is_paid', 'created_at']
    list_filter = ['status', 'is_paid', 'created_at']
    search_fields = ['full_name', 'phone_number', 'delivery_address']
    list_editable = ['status', 'is_paid'] # Let admin change status directly from the list!
    inlines = [OrderItemInline] # Connect the inline here