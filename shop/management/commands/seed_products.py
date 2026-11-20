
from django.core.management.base import BaseCommand
from shop.models import Product


class Command(BaseCommand):

    help = "Create sample shopping products"

    def handle(self, *args, **options):

        products = [
            {
                "name": "Wireless Keyboard",
                "description": "Comfortable wireless keyboard for everyday work.",
                "price": "899.00",
                "stock": 10,
            },
            {
                "name": "Gaming Mouse",
                "description": "High precision mouse for gaming and productivity.",
                "price": "599.00",
                "stock": 15,
            },
            {
                "name": "Bluetooth Headphones",
                "description": "Wireless headphones with clear sound quality.",
                "price": "1499.00",
                "stock": 8,
            },
        ]

        for data in products:

            product, created = Product.objects.get_or_create(
                name=data["name"],
                defaults={
                    "description": data["description"],
                    "price": data["price"],
                    "stock": data["stock"],
                    "is_available": True,
                }
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created: {product.name}"
                    )
                )
            else:
                self.stdout.write(
                    f"Already exists: {product.name}"
                )

        self.stdout.write(
            self.style.SUCCESS("Sample product seeding completed!")
        )
