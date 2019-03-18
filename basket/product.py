"""Product module."""


class Product:
    """Class that encapsulates a product item to be purchased."""

    def __init__(self, name, price, unit):
        """
        Given a name, price and unit constructs a product that can be
        used in purchases.

        :param name: Name of the product.
        :param price: Price of the product in pence.
        :param unit: The product's unit of quantity, e.g. bag or loaf.
        """
        self.name = name.lower()
        self.price = int(price)  # Assumed price is in pence
        self.unit = unit.lower()
        self._promotion = None

    def apply_promotion(self, promotion):
        """Apply an offer to this product.

        :param: promotion.Promotion instance.
        """
        self._promotion = promotion

    def clear_promotion(self):
        """Remove any promotion applied to this product."""
        self._promotion = None

    @property
    def has_promotion(self):
        """Check if product has a promotion applied.

        :return: True if the product has a promotion applied and
          False otherwise.
        """
        return self._promotion is not None

    @property
    def discounted_price(self):
        """The product price with discount applied.

        :return: Price in pence.
        """
        if self._promotion:
            return int(self.price - self.discount_amount)
        return self.price

    @property
    def discount_amount(self):
        """The amount of discount earned.

        :return: Discount amount in pence.
        """
        if self._promotion:
            return int(self.price * self._promotion.discount_percent / 100.0)
        return 0

    @property
    def discount_message(self):
        """Returns a message that represents the applied promotion.

        :return: String message.
        """
        discount_amount_str = '-£{:.2f}'.format(self.discount_amount/100)
        if self.discount_amount < 100:
            discount_amount_str = '-{}p'.format(self.discount_amount)
        if self._promotion:
            return '{}: {}'.format(
                self._promotion.title, discount_amount_str)
        return None
