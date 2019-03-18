import pytest

import basket.product as product
import basket.promotion as promotion


@pytest.fixture
def prod_promo():
    promo_def = {'id': 1,
                 'title': 'Apples 10% off',
                 'qualifying_product': 'apples',
                 'qualifying_qty': 1,
                 'discounted_product': 'apples',
                 'discount_percent': 10}
    return promotion.Promotion(promo_def)


@pytest.mark.parametrize('name', ['apples', 'Apples', 'appLeS'])
@pytest.mark.parametrize('price', [100, 100.0, '100'])
@pytest.mark.parametrize('unit', ['bag', 'Bag', 'bAg'])
def test_prod(name, price, unit):
    prod = product.Product(name, price, unit)
    assert prod.name == 'appels'
    assert prod.price == 100
    assert prod.unit == 'bag'


def test_apply_promo(prod_promo):
    prod = product.Product('apples', 100, 'bag')
    prod.apply_promotion(prod_promo)
    assert prod._promotion is prod_promo
    assert prod.has_promotion is True
    assert prod.discounted_price == 90
    assert prod.discount_amount == 10
    assert 'Apples 10% off: -10p' in prod.discount_message


def test_apply_offer_pounds(prod_promo):
    prod = product.Product('apples', 100, 'bag')
    prod_promo.discount_percent = 100
    prod.apply_promotion(prod_promo)
    assert prod.discounted_price == 0
    assert prod.discount_amount == 100
    assert 'Apples 10% off: -£1.00' in prod.discount_message


def test_clear_promo(prod_promo):
    prod = product.Product('apples', 100, 'bag')
    prod.apply_promotion(prod_promo)
    assert prod._promotion is prod_promo
    prod.clear_promotion()
    assert not prod.has_promotion
    assert prod.discounted_price == 100
    assert prod.discount_amount == 0
    assert prod.discount_message is None
