from rest_framework import serializers
from .models import Cart, CartItem, Order, PaymentMethod
from product.serializers import ProductSerializer
from .utils import remove_zero_quantity_items
class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = '__all__'

    def get_total_price(self, obj):
        # Очистка товаров с нулевым количеством перед расчетом общей стоимости
        remove_zero_quantity_items(obj)

        total = 0
        # Получаем все товары для данной корзины
        cart_items = CartItem.objects.filter(cart=obj)

        for item in cart_items:
            # Если есть скидка, то учитываем ее
            product_price = float(item.product.promotion) if item.product.promotion else float(item.product.price)
            total += product_price * item.quantity  # Умножаем цену на количество

        return total
class CartItemsSerializer(serializers.ModelSerializer):
    cart_id = serializers.IntegerField(source='cart.id', read_only=True)
    product = ProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()  # Добавим поле total_price

    class Meta:
        model = CartItem
        fields = ['cart_id', 'product', 'total_price', 'quantity', 'isOrder', 'user']  # Включаем total_price вместо price

    def get_total_price(self, obj):
        """
        Рассчитываем итоговую стоимость для каждого элемента в корзине.
        """
        product_price = float(obj.product.promotion) if obj.product.promotion else float(obj.product.price)
        return product_price * obj.quantity  # Возвращаем цену с учетом количества товара

    def create(self, validated_data):
        cart = validated_data.get('cart')
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')
        user = self.context['request'].user

        # Проверка на наличие достаточного количества товара
        self._check_stock_availability(product, quantity)

        # Устанавливаем цену с учетом промо-цены
        price = product.promotion if product.promotion is not None else product.price
        total_price = price * quantity

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity, 'price': total_price, 'user': user}
        )

        if not created:
            # Если элемент уже существует, обновляем количество и цену
            self._update_existing_cart_item(cart_item, product, quantity, price)
        else:
            # Если элемент был создан, уменьшаем количество товара на складе
            product.quantity -= quantity
            product.save()

        # Пересчитываем общую стоимость корзины
        self._update_cart_total_price(cart)

        return cart_item

    def update(self, instance, validated_data):
        new_quantity = validated_data.get('quantity', instance.quantity)
        product = instance.product

        if new_quantity != instance.quantity:
            # Проверка на достаточное количество товара
            self._check_stock_availability(product, new_quantity)

            # Обновляем количество товара на складе
            product.quantity += instance.quantity - new_quantity

            # Устанавливаем цену с учетом промо-цены
            price = product.promotion if product.promotion is not None else product.price
            instance.price = price * new_quantity

            instance.quantity = new_quantity
            product.save()
            instance.save()

            # Пересчитываем общую стоимость корзины
            self._update_cart_total_price(instance.cart)

        return instance


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
        order = Order.objects.create(**validated_data)
        order.clear_user_cart()  # Очистка корзины пользователя после создания заказа
        order.send_order_email()  # Отправка уведомления на почту
        return order
