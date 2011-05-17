# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from shop.util.fields import CurrencyField 
from shop.models.productmodel import Product

# Create your models here.

#==============================================================================
# Models
#==============================================================================

class Currency(models.Model):
    """
    A Currency. It is made of: 
    * a Name (for long display) 
    * a short name (i.e. "CHF", "USD"...)
    * a symbol, to display next to the price ("CHF","$","€"...)
    It can also be prefixed ("CHF152", "$123") or suffixed ("123£"). Deciding
    which currency should be prefixed and when is left as an excercise to the
    reader.
    """
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10) # Should be short
    prefix = models.BooleanField(default=False) # Should the symbol be prefixed?

class Price(models.Model):
    """
    A class representing a Price. A price is made of a value (the numerical
    part), and a currency. They are tied to a product.
    """
    # Product is polymorphic, so this is actually a key to Product subclasses
    product = models.ForeignKey(Product)
    value = CurrencyField() # What a poor naming choice :(
    currency = models.ForeignKey(Currency)

    def __unicode__(self):
        if self.currency.prefix:
            return "%s%s" % (self.currency.symbol, self.value)
        else:
            return "%s%s" % (self.value, self.currency.symbol)

#==============================================================================
# Mixins
#==============================================================================

class MultipleCurrencyMixin(object):
    """
    A mixin to add to your product subclasses to make them multi-currencies
    aware.
    You need to use this in your models in the following way:

    >> class MyProduct(Product, MultipleCurrencyMixin):
    >>     pass
    """

    def get_price(self):
        """
        Overrides the priduct's default get_price() method, in order to inject
        the multi-currency behavior.
        """
        if settings.SHOP_DEFAULT_CURRENCY:
            return self.get_price_in_currency(settings.SHOP_DEFAULT_CURRENCY)
        else:
            # Maybe the user put this mixin in by mistake, fallback to default
            # behavior
            return self.unit_price

    def get_price_in_currency(self, short_name):
        """
        Returns the price for this product in the currency matching `short_name`
        """
        price = Price.objects.filter(product=self,
            currency__short_name=short_name).select_related('currency')
        if len(price):
            price = price[0] 

        return price # Caller should "unpack" the information
