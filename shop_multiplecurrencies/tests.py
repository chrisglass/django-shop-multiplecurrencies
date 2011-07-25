# -*- coding: utf-8 -*-
from django.test import TestCase
from django.db import models
from decimal import Decimal
from shop_multiplecurrencies.models import Currency, Price, MultipleCurrencyMixin
from shop.models.productmodel import Product

class MultipleCurrencyTestModel(MultipleCurrencyMixin, Product):
    """
    A test model to assert the mixin's methods function properly. It doesn't do
    much
    """
    awesome_field = models.CharField(max_length=255)


class MultiCurrencyTestCase(TestCase):

    def setUp(self):
        self.currency = Currency.objects.create(
                            name='Bitcoin', # it's all the rage theses days
                            short_name="BTC",
                            symbol="BTC",
                        )

        self.product = Product.objects.create()

        self.price = Price.objects.create(
                        currency=self.currency,
                        product=self.product,
                        value=Decimal('99.99') # visible enough...
                    )

        self.instance = MultipleCurrencyTestModel.objects.create(
                            awesome_field='whatever'
                        )

    def test_check_currency_unicode(self):
        # simple enough - check that a currency's display is adequate
        self.assertEqual(str(self.price), '99.99BTC')
    
    def test_check_currency_unicode_with_prefix(self):
        # simple enough - check that a currency's display is adequate
        self.currency.prefix = True
        self.currency.save()
        self.assertEqual(str(self.price), 'BTC99.99')

    def test_check_currency_mixin_default_behavior(self):
        res = self.instance.get_price()
        self.assertEqual(res, self.instance.unit_price)

    def test_check_currency_mixin_get_price_in_currency(self):
        res = self.instance.get_price_in_currency('BTC')
        self.assertEqual(res, self.instance.unit_price)
