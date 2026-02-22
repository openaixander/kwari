from django.core.management.base import BaseCommand
from products.models import Category, Product

class Command(BaseCommand):
    help = 'Seeds the database with dummy categories and products for testing.'

    def handle(self, *args, **options):
        # 1. Create Categories (Foolproof direct assignment)
        cat_textiles, _ = Category.objects.get_or_create(slug="textiles", defaults={"name": "Textiles & Fabrics"})
        cat_footwear, _ = Category.objects.get_or_create(slug="footwear", defaults={"name": "Leather Footwear"})
        cat_traditional, _ = Category.objects.get_or_create(slug="traditional", defaults={"name": "Traditional Attire"})
        cat_jewelry, _ = Category.objects.get_or_create(slug="jewelry", defaults={"name": "Jewelry"})
        cat_accessories, _ = Category.objects.get_or_create(slug="accessories", defaults={"name": "Accessories"})

        # 2. Create Products using the exact variables above
        products_data = [
            # Textiles
            {"category": cat_textiles, "name": "Premium Ankara Wax", "slug": "premium-ankara", "price": 8500.00, "stock": 50, "description": "High-quality vibrant Ankara fabric, 6 yards."},
            {"category": cat_textiles, "name": "Kampala Adire Fabric", "slug": "kampala-adire", "price": 12000.00, "stock": 30, "description": "Authentic hand-dyed Adire fabric."},
            
            # Footwear
            {"category": cat_footwear, "name": "Kano Pure Leather Slippers", "slug": "kano-leather-slippers", "price": 15000.00, "stock": 20, "description": "Handcrafted pure leather slippers from Kwari artisans."},
            {"category": cat_footwear, "name": "Men's Suede Loafers", "slug": "suede-loafers", "price": 22000.00, "stock": 15, "description": "Elegant suede loafers for traditional events."},
            
            # Traditional Attire
            {"category": cat_traditional, "name": "Silk Buba and Sokoto Set", "slug": "silk-buba-set", "price": 35000.00, "stock": 10, "description": "Luxurious two-piece traditional silk wear."},
            {"category": cat_traditional, "name": "Embroidered Agbada Complete", "slug": "embroidered-agbada", "price": 75000.00, "stock": 5, "description": "Full three-piece Agbada set with heavy embroidery."},
            
            # Jewelry
            {"category": cat_jewelry, "name": "Beaded Coral Traditional Necklace", "slug": "coral-necklace", "price": 18000.00, "stock": 25, "description": "Authentic coral beads for traditional weddings."},
            {"category": cat_jewelry, "name": "Gold-Plated Filigree Earrings", "slug": "gold-earrings", "price": 5500.00, "stock": 40, "description": "Lightweight traditional style earrings."},
            
            # Accessories
            {"category": cat_accessories, "name": "Handwoven Fulani Hat", "slug": "fulani-hat", "price": 4500.00, "stock": 15, "description": "Traditional wide-brimmed woven hat."},
            {"category": cat_accessories, "name": "Leather Rattan Handbag", "slug": "rattan-handbag", "price": 16500.00, "stock": 12, "description": "Beautiful woven handbag with leather straps."},
        ]

        # 3. Save to database securely
        for prod_data in products_data:
            Product.objects.get_or_create(slug=prod_data["slug"], defaults=prod_data)

        self.stdout.write(self.style.SUCCESS("✅ Successfully seeded 5 categories and 10 products!"))