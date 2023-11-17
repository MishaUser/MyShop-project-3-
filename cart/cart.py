from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart:
    def __init__(self, request):
        """
        Инициализировать корзину.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохранить пустую корзину в сеансе
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        # quantity - целое число с количеством товара
        # override_quantity - нужно ли заменить количество переданным количеством (True)
        # либо прибавить новое количество к существующему количеству (False)
        """
        Добавить товар в корзину либо обновить его количество.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quality': 0,
                                     'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quality'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # поместить сеанс как "измененный",
        # чтобы обеспечить его сохранение
        self.session.modified = True

    def remove(self, product):
        """
        Удалить товар из корзины и вызвать метод save(), 
        чтобы обновить корзину в сеансе.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Прокрутить товарные позиции корзины в цикле
        и получить товары из базы данных.
        """
        product_ids = self.cart.keys()
        # получить объекты product и добавить их в корзину
        products = Product.object.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quality']
            yield item

    def __len__(self):
        """
        Подсчитать все товарные позиции в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        """
        Подсчитать общую стоимость товаров.
        """
        return sum(Decimal(item['price']) * item['quantity']
                   for item in self.cart.values())
    
    def clear(self):
        # удалить корзину из сеанса
        del self.session[settings.CART_SESSION_ID]
        self.save()