from decimal import Decimal
from django.conf import settings
from products.models import Product


class Cart:
    
    def __init__(self, request):
        """
        Initialize the cart
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)


        if not cart:
            # save an empty cart in the session if none exists
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart

    
    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity
        """

        # we use the product ID as the key in our dictionary

        product_id = str(product.id)


        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        
        current_qty = self.cart[product_id]['quantity']

        if override_quantity:
            new_qty = quantity
        else:
            new_qty = current_qty + quantity

        if new_qty > product.stock:
            return False
        
        self.cart[product_id]['quantity'] = new_qty
        self.save()
        return True
    

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True
    
    def remove(self, product):
        """
        Remove a product from the cart
        """

        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over items in the cart and get the products from the database.
        This lets us loop over 'cart' in templates
        """

        product_ids = self.cart.keys()

        # Get the actual product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()


        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
        

    def __len__(self):
        """
        Count all items in the cart
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def clear(self):
        # Delete ONLY the cart key from the session dictionary
        del self.session[settings.CART_SESSION_ID]
        self.save() # Mark session as modified

    
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())