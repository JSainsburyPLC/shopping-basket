"""Basket.

Simple application that prices a basket of products taking into account
any special offers.  The program accepts a list of items in the basket
and outputs the subtotal, the special offer discounts and the final price.

Information about products available for purchase (product names, units and
price) are loaded (by default) from the json file `products.json`.  Special
offers are are loaded (by default) from the json file `promotions.json`.
"""


import argparse
import json
import sys
import time

from basket import product
from basket import promotion
from basket import basket


class SimpleLogger:
    enabled = False
    info = 'INFO'
    error = 'ERROR'

    def log(self, message, level=info):
        """Simple logger.

        :param str message: Log message
        :param str level: Log level name
        """
        if self.enabled:
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            print('{} {}: {}'.format(now, level, message))


logger = SimpleLogger()


def parse_args(argv=None):
    """Parse command line arguments.

    :param list argv: Args to parse.
    """
    parser = argparse.ArgumentParser(prog='basket')
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=f'{parser.prog} 0.1',
    )
    parser.add_argument(
        '--products',
        help='Path of the products json file',
        default='products.json',
        dest='products',
    )
    parser.add_argument(
        '--promotions',
        help='Path of the promotions json file',
        default='promotions.json',
        dest='promotions',
    )
    parser.add_argument(
        'items',
        metavar='item',
        type=str,
        nargs='+',
        help='One or more items for the basket.  Only items listed in '
             'goods.json are accepted.')
    parser.add_argument(
        '--verbose',
        help='Verbose output',
        default=False,
        action='store_true',
        dest='verbose',
    )
    return parser.parse_args(argv)


def load_json(json_file_path):
    """Load json data.

    :param str json_file_path: Path to json file to load.
    """
    data = None
    try:
        with open(json_file_path) as f:
            data = json.load(f)
    except EnvironmentError:
        logger.log(f'No such file or directory: {json_file_path}',
                   SimpleLogger.error)
    except json.JSONDecodeError as e:
        logger.log(f'Failed to parse data file {json_file_path}: {e}',
                   SimpleLogger.error)
    return data


def load_products(products_file_path):
    """Load product definitions.

    Load product definition data describing the products this program will
    accept including product names, units and price.

    :param str products_file_path: Path to goods file.
    :return dict: Dictionary of product.Product instances.
    """
    products = {}
    data = load_json(products_file_path)
    if data is None:
        logger.log('No stock found in product data')
    else:
        # Build products list
        for prod in data:
            try:
                p = product.Product(prod['name'], prod['price'], prod['unit'])
                products[p.name] = p
            except ValueError as e:
                logger.log(f'Failed to load a product with data: {prod} ({e})',
                           SimpleLogger.error)
    return products


def load_promotions(promotions_file_path):
    """Load promotions.

    Load promotions data that specifies discounts that can be applied
    to goods purchased.

    :param str promotions_file_path: Path to promotions file.
    :return list: List of promotion.Promotion instances.
    """
    promotions = []
    data = load_json(promotions_file_path)
    if data:
        for prod_promo in data:
            try:
                promotions.append(promotion.Promotion(prod_promo))
            except (ValueError, KeyError) as e:
                logger.log('Failed to load offer with data: '
                           f'{prod_promo} ({e})', SimpleLogger.error)
    return promotions


def main(argv=None):
    """Program entry point.

    Parses any arguments, invokes `load_products` and `load_promotions` (to
    load the available goods and offers) and constructs a `basket` instance,
    giving it the available products in stock (`products`) and any prevailing
    offers (`promotions`).  For each product item specified on the command line,
    we add it to the basket. When all items have been added we query `basket`
    for a sub-total, discounts that could be applied and total price, which is
    output.

    :param list argv: Command line arguments.
    """
    # Parse arguments
    args = parse_args(argv)
    logger.enabled = args.verbose

    # Load available goods and offers
    products = load_products(args.products)
    promotions = load_promotions(args.promotions)

    # Make a basket and fill
    shopping_basket = basket.Basket(products, promotions)
    for item in args.items:
        if not shopping_basket.add(item):
            logger.log(f'Item \'{item}\' not in stock')

    # Print the results
    print(f'Subtotal: £{shopping_basket.subtotal/100:.2f}')
    shopping_basket.calculate_discounts()
    if shopping_basket.discounted_items:
        for item in shopping_basket.discounted_items:
            print(item.discount_message)
    else:
        print('(No offers available)')
    print(f'Total: £{shopping_basket.total/100:.2f}')


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
