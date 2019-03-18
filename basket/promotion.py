"""Offer module."""


class Promotion:
    """Class that encapsulates a product promotion."""

    def __init__(self, promo_def):
        """
        Given a definition, constructs a product promotion that can be applied
        to purchases.

        :param promo_def: Dictionary like object defining the promotion and
          should include values for they keys `id`, `title`,
          `qualifying_product`, `qualifying_qty`, `discounted_product`
          and `discount_percent`.
        :raises: ValueError if the qualifying qty is invalid, KeyError if one
          of the required dict keys is missing.
        """
        self.promo_id = promo_def['id']
        self.title = promo_def['title']
        self.qualifying_product = promo_def['qualifying_product'].lower()
        self.qualifying_qty = int(promo_def['qualifying_qty'])
        if not self.qualifying_qty:
            raise KeyError('Unacceptable value for qualifying_qty')
        self.discounted_product = promo_def['discounted_product'].lower()
        self.discount_percent = float(promo_def['discount_percent'])
