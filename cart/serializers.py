from collections import defaultdict
from rest_framework import serializers
from .models import Cart, CartItem, Order, PaymentMethod
from product.serializers import ProductSerializer
from .utils import remove_zero_quantity_items
class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()  # Итоговая цена корзины с учетом одной скидки
    total_quantity = serializers.SerializerMethodField()
    cart_items = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()  # Полная стоимость без учета скидки

    class Meta:
        model = Cart
        fields = ['id', 'total_price', 'total_quantity', 'cart_items', 'subtotal']

    def get_total_price(self, obj):
        # Начальная сумма для всех товаров в корзине
        total_price = 0
        for item in obj.cartitem_set.all():
            # Учитываем скидку, если она есть; если нет, используем стандартную цену
            product_price = float(item.product.promotion) if item.product.promotion else float(item.product.price)
            # Умножаем цену на количество и добавляем к общей сумме
            total_price += product_price * item.quantity
        print(f"Calculated Total Price with discounts: {total_price}")  # Логирование итоговой цены
        return total_price

    def get_subtotal(self, obj):
        # Общая стоимость всех товаров без учета скидок
        subtotal = sum(item.product.price * item.quantity for item in obj.cartitem_set.all())
        return subtotal

    def get_total_quantity(self, obj):
        return sum(item.quantity for item in obj.cartitem_set.all())

    def get_cart_items(self, obj):
        items = obj.cartitem_set.select_related('product').all()
        cart_items_data = []
        for item in items:
            product_price = self.calculate_product_price(item.product)
            cart_items_data.append({
                'cart_id': item.cart.id,
                'product_id': item.product.id,
                'title': item.product.title,
                'image': item.product.image.url if item.product.image else None,
                'quantity': item.quantity,
                'price': product_price  # Цена одного товара с учетом скидки, если она есть
            })
        return cart_items_data

    def calculate_product_price(self, product):
        """Вычисляет цену товара с учетом скидки"""
        return product.promotion if product.promotion else product.price


class CartItemsSerializer(serializers.ModelSerializer):
    cart_id = serializers.IntegerField(source='cart.id', read_only=True)
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    title = serializers.CharField(source='product.title', read_only=True)
    image = serializers.SerializerMethodField()
    quantity = serializers.IntegerField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['cart_id', 'product_id', 'title', 'image', 'quantity', 'price']

    def get_image(self, obj):
        return self.get_product_image(obj.product)

    def get_price(self, obj):
        product_price = self.calculate_product_price(obj.product)
        return product_price * obj.quantity

    def calculate_product_price(self, product):
        """Метод для вычисления цены товара с учетом скидки"""
        return product.promotion if product.promotion else product.price

    def get_product_image(self, product):
        """Проверяем изображения по порядку"""
        if product.image1:
            return product.image1.url
        elif product.image2:
            return product.image2.url
        elif product.image3:
            return product.image3.url
        return None
class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['id', 'name']

class OrderSerializer(serializers.ModelSerializer):
    payment_method = serializers.PrimaryKeyRelatedField(queryset=PaymentMethod.objects.all())

    class Meta:
        model = Order
        fields = ['user', 'cart', 'total_price', 'address', 'payment_method']

    def create(self, validated_data):
        cart = validated_data.get('cart')

        # Проверка на пустую корзину
        if cart.cartitem_set.count() == 0:
            raise serializers.ValidationError("Корзина пуста. Невозможно создать заказ.")

        order = Order.objects.create(**validated_data)

        # Уменьшение количества товаров на складе при создании заказа
        for item in order.cart.cartitem_set.all():
            item.product.quantity -= item.quantity
            item.product.save()

        order.clear_user_cart()  # Очистка корзины пользователя после создания заказа
        order.send_order_email()  # Отправка уведомления на почту

        return order
