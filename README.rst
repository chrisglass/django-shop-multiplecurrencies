==============================
django-shop-multiplecurrencies
==============================

This companion application to django-shop adds support for multiple currencies
to project needing/wanting such a feature.

Installation
============

* Run `pip install django-shop-multiplecurrencies`
* Add `shop_multiplecurrencies` to your INSTALLED_APPS
* Mix your Django models in with the provided `MultipleCurrencyMixin`
* ???
* Profit!!!

Displaying multi-currency prices
================================

To display your prices in a specific currency, use the following template tag::

    {% import shop_multiplecurrency %}

    <!--- We assume there is a `product` object in the context --->
    {% price product.price 'chf' %} <!-- This will display the proce in CHF-->
    {% price product.price %}
