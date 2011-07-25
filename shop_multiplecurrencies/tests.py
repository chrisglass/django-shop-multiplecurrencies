# -*- coding: utf-8 -*-
from django.test import TestCase
from django.db import models
from shop_multiplecurrencies.models import Currency, Price, MultipleCurrencyMixin
from shop.models.productmodel import Product

class MultipleCurrencyTestModel(Product, MultipleCurrencyMixin):
    """
    A test model to assert the mixin's methods function properly. It doesn't do
    much
    """
    awesome_field = models.CharField(max_length=255)


class MultiCurrencyTestCase(TestCase):

    def setUp(self):
        self.currency = Currency.objects.create(name='Bitcoin',
                        short_name="BTC",
                        symbol="BTC",
                        )

        self.product = Product.objects.create()
        self.price = Price.objects.create(
                        currency=self.currency,
                        product=self.product
                    )
        self.instance = MultipleCurrencyTestModel.objects.create()

    def test_check_currency_unicode(self):
        # simple enough - check that a currency's display is adequate
        self.assertEqual(str(self.price), '0.00BTC')
    
    def test_check_currency_unicode_with_prefix(self):
        # simple enough - check that a currency's display is adequate
        self.currency.prefix = True
        self.currency.save()
        self.assertEqual(str(self.price), 'BTC0.00')

    def test_check_currency_mixin_default_behavior(self):
        res = self.instance.get_price()
        self.assertEqual(res, self.instance.unit_price)

    def test_check_currency_mixin_get_price_in_currency(self):
        res = self.instance.get_price_in_currency('BTC')
        self.assertEqual(res, self.instance.unit_price)
