from django.db import models
from shop.util.fields import CurrencyField 
from shop.models.productmodels import Product

# Create your models here.

class Currency(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10) # Should be short
    prefix = models.Boolean(default=False) # Should the symbol be prefixed?

class Price(models.Model):
    """
    A class representing a Price. A price is made of a value (the numerical
    part), and a currency. They are tied to a product.
    """
    # Product is polymorphic, so this is actually a key to Product subclasses
    product = models.ForeignKey(Product)
    value = CurrencyField()
    currency = models.ForeignKey(Currency)

    def __unicode__(self):
        if self.currency.prefix:
            return "%s%s" % (self.currency.symbol, self.value)
        else:
            return "%s%s" % (self.value, self.currency.symbol)


class MultipleCurrencyMixin(object):
    """
    A mixin to add to your product subclasses to make them multi-currencies
    aware.
    """
    def get_price(self):
        pass # TODO: Use a default currency setting or something

    def get_price_in_currency(self, symbol):
        """
        Returns the price for this product in the currency matching `symbol`
        """
        price = Price.objects.filter(product=self, currency__symbol=symbol)
        if len(price):
            price = price[0] 
