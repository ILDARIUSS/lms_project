import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(name: str):
    return stripe.Product.create(name=name)


def create_stripe_price(product_id: str, amount: int):
    return stripe.Price.create(
        unit_amount=amount * 100,
        currency='usd',
        product=product_id,
    )


def create_stripe_session(price_id: str):
    return stripe.checkout.Session.create(
        success_url='http://127.0.0.1:8000/success/',
        cancel_url='http://127.0.0.1:8000/cancel/',
        line_items=[
            {
                'price': price_id,
                'quantity': 1,
            }
        ],
        mode='payment',
    )