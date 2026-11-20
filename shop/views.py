
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import Product
from .cart import get_cart


def product_list(request):

    products = Product.objects.filter(
        is_available=True,
        stock__gt=0
    )

    return render(
        request,
        "shop/product_list.html",
        {"products": products}
    )


@require_POST
def cart_add(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True,
        stock__gt=0
    )

    cart = request.session.get("shopping_cart", {})
    key = str(product.id)

    current_quantity = int(cart.get(key, 0))

    if current_quantity < product.stock:
        cart[key] = current_quantity + 1
        request.session["shopping_cart"] = cart
        messages.success(request, "Product added to cart!")
    else:
        messages.warning(request, "Maximum available stock reached.")

    return redirect("shop:product_list")


def cart_detail(request):

    items, total = get_cart(request)

    return render(
        request,
        "shop/cart_detail.html",
        {
            "items": items,
            "total": total,
        }
    )


@require_POST
def cart_update(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get("shopping_cart", {})
    key = str(product.id)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (ValueError, TypeError):
        messages.error(request, "Please enter a valid quantity.")
        return redirect("shop:cart_detail")

    if quantity <= 0:
        cart.pop(key, None)
        messages.success(request, "Product removed from cart.")

    elif not product.is_available or product.stock <= 0:
        cart.pop(key, None)
        messages.warning(request, "This product is no longer available.")

    elif quantity > product.stock:
        cart[key] = product.stock
        messages.warning(
            request,
            f"Only {product.stock} units are available."
        )

    else:
        cart[key] = quantity
        messages.success(request, "Cart updated successfully.")

    request.session["shopping_cart"] = cart

    return redirect("shop:cart_detail")


@require_POST
def cart_remove(request, product_id):

    cart = request.session.get("shopping_cart", {})

    key = str(product_id)

    cart.pop(key, None)

    request.session["shopping_cart"] = cart

    messages.success(request, "Product removed from cart.")

    return redirect("shop:cart_detail")
