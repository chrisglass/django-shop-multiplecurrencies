from classytags.helpers import InclusionTags
from classtags.core import Options
from classtags.arguments import Argument
from django import template

register = template.Library()

class PriceTemplateTag(InclusionTags):
    """
    This will display a passed-in price (taken from a Product instance) and
    display it in the currency's preferred format.

    It includes `shop_multiplecurrencies/templatetags/_price.html` 
    """

    template = "shop_multiplecurrencies/templatetags/_price.html" 
    options = Options(
        Argument('price', resolve=True, required=True),
        Argument('currency', resolve=True, required=False), #The short_name
    )

    def get_context(self, context, price, currency=None):
        price_str = ''
        price_obj = None
        if currency:
            #Let's try and return the price for the specific currency:
            price_obj = price.get_price_in_currency(currency)
            price_str = str(price_obj)
        else:
            #Let's return the default price.
            price_obj = price.get_price()
            price_str = str(price_obj)

        return {'price', price_str}

register.tag(PriceTemplateTag)
