import time

import pytest

import basket.__main__ as main


@pytest.fixture
def products_json():
    return """[
    {
      "name": "Soup", "price": 65, "unit": "Tin"
    },
    {
      "name": "Bread", "price": 80, "unit": "Loaf"
    },
    {
      "name": "Milk", "price": 130, "unit": "Bottle"
    },
    {
      "name": "Apples", "price": 100, "unit": "Bag"
    }]"""


@pytest.fixture
def faulty_products_json():
    return """[
    {
      "name": "Apples", "price": "100.0", "unit": "Bag"
    }]"""


@pytest.fixture
def faulty_promo_json():
    return """[
    {
      "id": 1,
      "title": "Apples 10% off",
      "qualifying_product": "Apples",
      "qualifying_qty": 0,
      "discounted_product": "Apples",
      "discount_percent": 10
    }]"""


@pytest.fixture
def ok_json():
    return """[
    {
      "hello": "json", "int": 10, "float": 1.2, "list": [1, 2, 3]
    }]"""


@pytest.fixture
def bad_json():
    return 'foo'


@pytest.fixture
def promo_json():
    return """[
    {
      "id": 1,
      "title": "Apples 10% off",
      "qualifying_product": "Apples",
      "qualifying_qty": 1,
      "discounted_product": "Apples",
      "discount_percent": 10
    },
    {
      "id": 2,
      "title": "2 tins soup get you a half price loaf",
      "qualifying_product": "Soup",
      "qualifying_qty": 2,
      "discounted_product": "Bread",
      "discount_percent": 50
    }]"""


@pytest.fixture
def empty_json():
    return '[]'


@pytest.fixture
def ok_json_file(tmpdir, ok_json):
    tmpfile = tmpdir.join('ok.json')
    with tmpfile.open('w') as f:
        f.write(ok_json)
    return str(tmpfile)


@pytest.fixture
def bad_json_file(tmpdir, bad_json):
    tmpfile = tmpdir.join('bad.json')
    with tmpfile.open('w') as f:
        f.write(bad_json)
    return str(tmpfile)


@pytest.fixture
def products_json_file(tmpdir, products_json):
    tmpfile = tmpdir.join('products.json')
    with tmpfile.open('w') as f:
        f.write(products_json)
    return str(tmpfile)


@pytest.fixture
def faulty_products_json_file(tmpdir, faulty_products_json):
    tmpfile = tmpdir.join('faulty.json')
    with tmpfile.open('w') as f:
        f.write(faulty_products_json)
    return str(tmpfile)


@pytest.fixture
def promo_json_file(tmpdir, promo_json):
    tmpfile = tmpdir.join('promo.json')
    with tmpfile.open('w') as f:
        f.write(promo_json)
    return str(tmpfile)


@pytest.fixture
def faulty_promo_json_file(tmpdir, faulty_promo_json):
    tmpfile = tmpdir.join('faulty_promo.json')
    with tmpfile.open('w') as f:
        f.write(faulty_promo_json)
    return str(tmpfile)


@pytest.fixture
def empty_json_file(tmpdir, empty_json):
    tmpfile = tmpdir.join('empty.json')
    with tmpfile.open('w') as f:
        f.write(empty_json)
    return str(tmpfile)


def test_log(capsys):
    main.logger.enabled = True
    main.logger.log('foo')
    stdout, _ = capsys.readouterr()
    assert isinstance(time.strptime(stdout[:19], '%Y-%m-%d %H:%M:%S'),
                      time.struct_time)
    assert 'INFO: foo' in stdout


def test_log_error(capsys):
    main.LOGGING = True
    main.log('foo', level=main.ERROR)
    stdout, _ = capsys.readouterr()
    assert 'ERROR: foo' in stdout


def test_log_quiet(capsys):
    main.logger.enabled = False
    main.logger.log('foo')
    stdout, _ = capsys.readouterr()
    assert not len(stdout)


class TestParseArgs:

    def test_version(self, capsys):
        with pytest.raises(SystemExit):
            main.parse_args(['--version'])
        stdout, _ = capsys.readouterr()
        assert 'basket' in stdout

    def test_prod_default(self):
        args = main.parse_args(['apple'])
        assert args.products == 'products.json'

    def test_promo_default(self):
        args = main.parse_args(['apple'])
        assert args.promotions == 'promotions.json'

    def test_prod_override(self):
        args = main.parse_args(['--products=foo.json', 'apple'])
        assert args.products == 'foo.json'

    def test_promo_override(self):
        args = main.parse_args(['--promotions=foo.json', 'apple'])
        assert args.promotions == 'foo.json'

    def test_verbose(self):
        args = main.parse_args(['--verbose', 'apple'])
        assert args.verbose is True


def test_load_json(ok_json_file):
    assert main.load_json(ok_json_file) is not None


def test_load_json_no_file(capsys):
    main.logger.enabled = True
    assert main.load_json('foo.json') is None
    stdout, _ = capsys.readouterr()
    assert 'ERROR: No such file or directory: foo.json' in stdout


def test_load_json_bad_file(bad_json_file, capsys):
    main.LOGGING = True
    assert main.load_json(bad_json_file) is None
    stdout, _ = capsys.readouterr()
    assert 'ERROR: Failed to parse data file' in stdout
    assert 'bad.json' in stdout


def test_load_products(products_json_file):
    products = main.load_products(products_json_file)
    assert products
    assert len(products) == 4
    assert all(k in products for k in ('soup', 'bread', 'milk', 'apples'))
    assert products['soup'].price == 65
    assert products['soup'].unit == 'tin'
    assert products['bread'].price == 80
    assert products['bread'].unit == 'loaf'
    assert products['milk'].price == 130
    assert products['milk'].unit == 'bottle'
    assert products['apples'].price == 100
    assert products['apples'].unit == 'bag'


def test_load_products_no_stock(empty_json_file):
    products = main.load_products(empty_json_file)
    assert products == {}
    assert len(products) == 0


def test_load_prod_bad_item(faulty_products_json_file, capsys):
    main.LOGGING = True
    products = main.load_products(faulty_products_json_file)
    stdout, _ = capsys.readouterr()
    assert 'Failed to load a product with data' in stdout
    assert '(invalid literal for int() with base 10: \'100.0\'' in stdout
    assert len(products) == 0


def test_load_promo(promo_json_file):
    promotions = main.load_promotions(promo_json_file)
    assert promotions
    assert len(promotions) == 2
    assert promotions[0].promo_id == 1
    assert promotions[1].promo_id == 2
    assert promotions[0].title == 'Apples 10% off'
    assert promotions[1].title == '2 tins soup get you a half price loaf'


def test_load_offers_bad_item(faulty_promo_json_file, capsys):
    main.LOGGING = True
    offers = main.load_promotions(faulty_promo_json_file)
    stdout, _ = capsys.readouterr()
    assert 'Failed to load offer with data' in stdout
    assert '(Unacceptable value for qualifying_qty)' in stdout
    assert len(offers) == 0


def test_main(capsys):
    main.main(['apples'])
    stdout, _ = capsys.readouterr()
    expectd_op = 'Subtotal: £1.00\nApples 10% off: -10p\nTotal: £0.90'
    assert expectd_op in stdout


def test_main_unknown_prod(capsys):
    main.main(['pie', '--verbose'])
    stdout, _ = capsys.readouterr()
    expectd_op = ('INFO: Item \'pie\' not in stock\nSubtotal: £0.00\n'
                  '(No offers available)\nTotal: £0.00')
    assert expectd_op in stdout
