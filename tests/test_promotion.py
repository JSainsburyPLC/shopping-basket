import pytest

import basket.promotion as promotion


@pytest.mark.parametrize('qualifying_product', ['apples', 'Apples', 'appLeS'])
@pytest.mark.parametrize('qualifying_qty', [1, 1.0, '1'])
@pytest.mark.parametrize('discounted_product', ['appLes', 'Apples'])
@pytest.mark.parametrize('discount_percent', [10, '10', 10.0])
def test_offer(qualifying_product, qualifying_qty, discounted_product,
               discount_percent):
    offer_def = {'id': 1,
                 'title': 'Apples 10% off',
                 'qualifying_product': qualifying_product,
                 'qualifying_qty': qualifying_qty,
                 'discounted_product': discounted_product,
                 'discount_percent': discount_percent}
    p = promotion.Promotion(offer_def)
    assert p.promo_id == 1
    assert p.title == 'Apples 10% off'
    assert p.qualifying_product == 'apples'
    assert p.qualifying_qty == 1
    assert p.discounted_product == 'apples'
    assert p.discount_percent == 10


def test_bad_offer():
    promo_def = {'id': 1,
                 'title': 'Apples 10% off',
                 'qualifying_product': 'Apples',
                 'qualifying_qty': 0,
                 'discounted_product': 'Apples',
                 'discount_percent': 10}
    with pytest.raises(ValueError) as e:
        promotion.Promotion(promo_def)
    assert 'Unacceptable value for qualifying_qty' in str(e)
