from collections import defaultdict
from rest_framework import serializers
from .models import Cart, CartItem, Order, PaymentMethod
from product.serializers import ProductSerializer
from .utils import remove_zero_quantity_items

class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()
    cart_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'total_price', 'total_quantity', 'cart_items']  # Поля корзины

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

    def get_total_quantity(self, obj):
        """Возвращаем общее количество товаров в корзине."""
        return sum(item.quantity for item in obj.cartitem_set.all())

    def get_cart_items(self, obj):
        """Возвращаем список товаров с изображениями в корзине."""
        items = CartItem.objects.filter(cart=obj)
        cart_items_data = []
        for item in items:
            product_price = float(item.product.promotion) if item.product.promotion else float(item.product.price)
            cart_items_data.append({
                'productId': item.product.id,
                'title': item.product.title,
                'image': item.product.image.url if item.product.image else None,  # URL изображения товара
                'quantity': item.quantity,
                'price': product_price * item.quantity  # Общая стоимость для данного товара
            })
        return cart_items_data

class CartItemsSerializer(serializers.ModelSerializer):
    cart_id = serializers.IntegerField(source='cart.id', read_only=True)
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    title = serializers.CharField(source='product.title', read_only=True)
    image = serializers.SerializerMethodField()  # Добавляем поле для изображения
    quantity = serializers.IntegerField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['cart_id', 'product_id', 'title', 'image', 'quantity', 'price']  # Убираем ненужные поля

    def get_image(self, obj):
        """Возвращаем изображение товара."""
        return self.get_product_image(obj.product)

    def get_price(self, obj):
        """
        Рассчитываем итоговую стоимость для каждого элемента в корзине.
        """
        product_price = float(obj.product.promotion) if obj.product.promotion else float(obj.product.price)
        return product_price * obj.quantity

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
            cart_item.quantity += quantity
            cart_item.price = total_price
            cart_item.save()

        # Пересчитываем общую стоимость корзины
        self._update_cart_total_price(cart)

        return cart_item

    def update(self, instance, validated_data):
        new_quantity = validated_data.get('quantity', instance.quantity)
        product = instance.product

        if new_quantity != instance.quantity:
            # Проверка на достаточное количество товара
            self._check_stock_availability(product, new_quantity)

            # Устанавливаем цену с учетом промо-цены
            price = product.promotion if product.promotion is not None else product.price
            instance.price = price * new_quantity

            instance.quantity = new_quantity
            instance.save()

            # Пересчитываем общую стоимость корзины
            self._update_cart_total_price(instance.cart)

        return instance

    def _check_stock_availability(self, product, quantity):
        """Проверка на достаточное количество товара на складе."""
        if product.quantity < quantity:
            raise serializers.ValidationError(f"Недостаточно товара '{product.title}' на складе")

    def _update_cart_total_price(self, cart):
        """Обновляет общую стоимость корзины."""
        total_price = sum(
            (item.product.promotion or item.product.price) * item.quantity
            for item in cart.cartitem_set.all()
        )
        cart.total_price = total_price
        cart.save()

    def get_product_image(self, product):
        """Метод для выбора изображения товара (image1, image2, image3)."""
        if product.image1:
            return product.image1.url
        elif product.image2:
            return product.image2.url
        elif product.image3:
            return product.image3.url
        return None  # Если изображений нет
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
