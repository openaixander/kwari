from django.core.management.base import BaseCommand
from products.models import Category, Product

class Command(BaseCommand):
    help = 'Seeds the database with dummy categories and products for testing.'

    def handle(self, *args, **options):
        # 1. Create Categories
        categories_data = [
            {"name": "Textiles & Fabrics", "slug": "textiles"},
            {"name": "Leather Footwear", "slug": "footwear"},
            {"name": "Traditional Attire", "slug": "traditional"},
            {"name": "Jewelry", "slug": "jewelry"},
            {"name": "Accessories", "slug": "accessories"},
        ]

        category_objs = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(slug=cat_data["slug"], defaults=cat_data)
            category_objs[cat.slug] = cat

        # 2. Create Products
        products_data = [
            # Textiles
            {"category": category_objs["textiles"], "name": "Premium Ankara Wax", "slug": "premium-ankara", "price": 8500.00, "stock": 50, "description": "High-quality vibrant Ankara fabric, 6 yards."},
            {"category": category_objs["textiles"], "name": "Kampala Adire Fabric", "slug": "kampala-adire", "price": 12000.00, "stock": 30, "description": "Authentic hand-dyed Adire fabric."},
            
            # Footwear
            {"category": category_objs["footwear"], "name": "Kano Pure Leather Slippers", "slug": "kano-leather-slippers", "price": 15000.00, "stock": 20, "description": "Handcrafted pure leather slippers from Kwari artisans."},
            {"category": category_objs["footwear"], "name": "Men's Suede Loafers", "slug": "suede-loafers", "price": 22000.00, "stock": 15, "description": "Elegant suede loafers for traditional events."},
            
            # Traditional Attire
            {"category": category_objs["traditional"], "name": "Silk Buba and Sokoto Set", "slug": "silk-buba-set", "price": 35000.00, "stock": 10, "description": "Luxurious two-piece traditional silk wear."},
            {"category": category_objs["traditional"], "name": "Embroidered Agbada Complete", "slug": "embroidered-agbada", "price": 75000.00, "stock": 5, "description": "Full three-piece Agbada set with heavy embroidery."},
            
            # Jewelry
            {"category": category_objs["jewelry"], "name": "Beaded Coral Traditional Necklace", "slug": "coral-necklace", "price": 18000.00, "stock": 25, "description": "Authentic coral beads for traditional weddings."},
            {"category": category_objs["jewelry"], "name": "Gold-Plated Filigree Earrings", "slug": "gold-earrings", "price": 5500.00, "stock": 40, "description": "Lightweight traditional style earrings."},
            
            # Accessories
            {"category": category_objs["accessories"], "name": "Handwoven Fulani Hat", "slug": "fulani-hat", "price": 4500.00, "stock": 15, "description": "Traditional wide-brimmed woven hat."},
            {"category": category_objs["accessories"], "name": "Leather Rattan Handbag", "slug": "rattan-handbag", "price": 16500.00, "stock": 12, "description": "Beautiful woven handbag with leather straps."},
        ]

        for prod_data in products_data:
            Product.objects.get_or_create(slug=prod_data["slug"], defaults=prod_data)

        self.stdout.write(self.style.SUCCESS("✅ Successfully seeded 5 categories and 10 products!"))