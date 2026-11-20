
from .models import Product


def get_cart(request):

    cart_data = request.session.get("shopping_cart", {})

    product_ids = cart_data.keys()

    products = Product.objects.filter(
        id__in=product_ids,
        is_available=True
    )

    items = []
    total = 0

    for product in products:

        quantity = int(cart_data.get(str(product.id), 0))

        # Limit quantity to available stock
        quantity = min(quantity, product.stock)

        if quantity <= 0:
            continue

        line_total = product.price * quantity

        items.append({
            "product": product,
            "quantity": quantity,
            "line_total": line_total,
        })

        total += line_total

    return items, total
