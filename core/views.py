from django.shortcuts import render
from django.db.models import Q
from products.models import Category, Product
# Create your views here.

def index(request):
    # now we are going to make the index.html page dynamic

    # fetch featured products(limit to 8 to not overcrowd the page)

    featured_products = Product.objects.filter(is_featured=True).select_related('category')[:8]

    query = request.GET.get('q')

    # let's check and see if query exist

    if query:
        featured_products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).select_related('category')

    else:
        featured_products = featured_products[:8]

    categories = Category.objects.all()[:3]


    context = {
        'featured_products':featured_products,
        'categories':categories,
        'search_query': query,
        }
    return render(request, 'core/index.html', context)
