import requests
from django.conf import settings


def create_stripe_product(name: str):
    url = 'https://api.stripe.com/v1/products'

    data = {
        'name': name
    }

    response = requests.post(
        url,
        data=data,
        auth=(settings.STRIPE_SECRET_KEY, '')
    )

    return response.json()


def create_stripe_price(product_id: str, amount: int):
    url = 'https://api.stripe.com/v1/prices'

    data = {
        'unit_amount': amount * 100,
        'currency': 'usd',
        'product': product_id,
    }

    response = requests.post(
        url,
        data=data,
        auth=(settings.STRIPE_SECRET_KEY, '')
    )

    return response.json()


def create_stripe_session(price_id: str):
    url = 'https://api.stripe.com/v1/checkout/sessions'

    data = {
        'success_url': 'https://example.com/success',
        'cancel_url': 'https://example.com/cancel',
        'line_items[0][price]': price_id,
        'line_items[0][quantity]': 1,
        'mode': 'payment',
    }

    response = requests.post(
        url,
        data=data,
        auth=(settings.STRIPE_SECRET_KEY, '')
    )

    return response.json()