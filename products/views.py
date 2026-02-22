from django.shortcuts import render, get_object_or_404

from .models import Product, Category

# Create your views here.

def product_list(request, category_slug=None):
    """
    This is the view that helps retrieves all product from the db
    
    
    :param category_slug: This is passed when the user clicks on a particular category
    """
    category = None
    categories = Category.objects.all()
    products = Product.objects.select_related('category')


    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        # narrow our products to be based on that category
        products = products.filter(category=category)
    


    
    # now time to check the when to ascend or descend

    sort_option = request.GET.get('sort')

    if sort_option == 'price-low':
        products = products.order_by('price')
    elif sort_option == 'price-high':
        products = products.order_by('-price')
    elif sort_option == 'newest':
        products = products.order_by('-created_at')
    
    else:
        # default sort(if no option selected)
        products = products.order_by('-is_featured', '-created_at')
        sort_option = 'newest'
    
    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'current_sort':sort_option
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, slug):
    """
    This helps in showing the a particular product in full
    
    :param request: Description
    :param slug: This is the slug created which is passed when a user wants to see the whole of the product
    """


    product = get_object_or_404(Product.objects.select_related('category'), slug=slug)

    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }

    return render(request, 'products/product_detail.html', context)