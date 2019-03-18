import pytest

import basket.basket as basket
import basket.product as product
import basket.promotion as promotion


@pytest.fixture
def products():
    return {
      'soup': product.Product('soup', 65, 'tin'),
      'bread': product.Product('bread', 80, 'loaf'),
      'milk': product.Product('milk', 130, 'bottle'),
      'apples': product.Product('apples', 100, 'bag'), }


@pytest.fixture
def products_empty():
    return {}


@pytest.fixture
def promo_def():
    return {'id': 1, 'title': 'Apples 10% off',
            'qualifying_product': 'apples',
            'qualifying_qty': 1,
            'discounted_product': 'apples',
            'discount_percent': 10}


@pytest.fixture
def promotions(promo_def):
    return [promotion.Promotion(promo_def)]


@pytest.fixture
def promotions_empty():
    return []


def test_basket(products, promotions):
    b = basket.Basket(products, promotions)
    assert b.products is products
    assert b.products is products
    assert b.items == []
    assert b.discounts == []


def test_add_item(products, promotions):
    b = basket.Basket(products, promotions)
    assert b.add('apples')
    assert len(b.items) == 1
    assert b.subtotal == 100
    assert b.total == 100


def test_add_item_no_products(products_empty, promotions):
    b = basket.Basket(products_empty, promotions)
    assert b.products is products_empty
    assert b.promotions is promotions
    assert b.add('apples') is False


def test_add_item_no_promotions(products, promotions_empty):
    b = basket.Basket(products, promotions_empty)
    assert b.products is products
    assert b.promotions is promotions_empty
    assert b.add('apples')
    b.calculate_discounts()
    assert b.subtotal == 100
    assert b.total == 100
    assert not len(b.discounted_items)


def test_discount(products, promotions):
    b = basket.Basket(products, promotions)
    assert b.add('apples')
    assert len(b.items) == 1
    assert b.subtotal == 100
    b.calculate_discounts()
    assert b.total == 90
    assert len(b.discounted_items) == 1
    assert b.discounted_items[0] is b.items[0]


def test_add_items_discount(products, promotions):
    b = basket.Basket(products, promotions)
    assert b.add('apples')
    assert b.add('apples')
    assert len(b.items) == 2
    assert b.subtotal == 200
    b.calculate_discounts()
    assert b.total == 180
    assert len(b.discounted_items) == 2
    assert b.discounted_items[0] is b.items[0]
    assert b.discounted_items[1] is b.items[1]
