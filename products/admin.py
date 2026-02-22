from django.contrib import admin
from .models import Category, Product
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']

    # prepopulated_fields = {
    #     'slug' : ('name',)
    # }

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'price',
        'stock',
        'category',
        'is_featured',
        'updated_at',
        'slug'
        ]
    
    list_editable = [
        'price',
        'stock',
        'is_featured'
        ]
    
    # prepopulated_fields = {
    #     'slug' : ('name',)
    #     }

    list_filter = [
        'is_featured',
        'category',
        'created_at',
        ]
    
    search_fields = ['name', 'description']
