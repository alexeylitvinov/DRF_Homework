import stripe

from config.settings import STRIPE_KEY

stripe.api_key = STRIPE_KEY


def create_price(price):
    """
    Создание цены для оплаты
    """
    return stripe.Price.create(
        currency="rub",
        unit_amount=price * 100,
        product_data={"name": "Payment_for_course"},
    )


def create_stripe_session(price):
    """
    Создание сессии на оплату
    """
    session = stripe.checkout.Session.create(
        line_items=[{
            'price': price.get('id'),
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/',
        cancel_url='http://127.0.0.1:8000/',
    )
    return session.get('url'), session.get('id')
