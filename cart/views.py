from django.shortcuts import render

from .models import Order, Cart
from .serializers import OrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from product.models import Product
from .serializers import CartSerializer, CartItemsSerializer
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['cart'],
        operation_description="Этот эндпоинт позволяет получить список элементов," 
                              "которые есть в корзине пользователя."
    )
    def get(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user, ordered=False).first()
        queryset = CartItem.objects.filter(cart=cart)
        serializer = CartItemsSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=['cart'],
        operation_description="Этот эндпоинт позволяет добавить определенный товар,"
                              "в корзину пользователя."
    )
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user, ordered=False)

        product = get_object_or_404(Product, id=data.get('product'))
        quantity = data.get('quantity')

        # Получаем цену товара и проверяем, применима ли акция
        price = product.price
        promotion = product.promotion if product.promotion else 0  # предполагается, что `promotion` - процент

        # Применяем акцию, если она есть
        if promotion > 0:
            price = price * (1 - promotion / 100)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            user=user,
            product=product,
            defaults={'price': price, 'quantity': quantity}
        )

        if not created:
            # Обновляем существующий элемент
            cart_item.quantity += quantity
            cart_item.price = price * cart_item.quantity
            cart_item.save()

        # Пересчитываем общую цену в корзине
        total_price = sum(item.price for item in CartItem.objects.filter(cart=cart))
        cart.total_price = total_price
        cart.save()

        return Response({'success': 'Item added to your cart'})

    @swagger_auto_schema(
        tags=['cart'],
        operation_description="Этот эндпоинт позволяет изменить/обновить товар,"
                              "который находится в корзине пользователя."
    )
    def put(self, request):
        data = request.data
        cart_item = get_object_or_404(CartItem, id=data.get('id'))
        quantity = data.get('quantity')

        product = cart_item.product
        price = product.price
        promotion = product.promotion if product.promotion else 0

        # Применяем акцию, если она есть
        if promotion > 0:
            price = price * (1 - promotion / 100)

        # Обновляем количество и цену
        cart_item.quantity = quantity
        cart_item.price = price * quantity
        cart_item.save()

        # Пересчитываем общую цену в корзине
        cart = cart_item.cart
        total_price = sum(item.price for item in CartItem.objects.filter(cart=cart))
        cart.total_price = total_price
        cart.save()

        return Response({'success': 'Product updated'})

    @swagger_auto_schema(
        tags=['cart'],
        operation_description="Этот эндпоинт позволяет удалить товар,"
                              "с корзины пользователя."
    )
    def delete(self, request):
        user = request.user
        data = request.data

        cart_item = get_object_or_404(CartItem, id=data.get('id'))
        cart_item.delete()

        cart = Cart.objects.filter(user=user, ordered=False).first()
        queryset = CartItem.objects.filter(cart=cart)
        serializer = CartItemsSerializer(queryset, many=True)
        return Response(serializer.data)

#order

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user, ordered=False).first()

        if not cart:
            return Response({'error': 'Cart not found or already ordered'}, status=400)

        # Создаём заказ
        order = Order.objects.create(
            user=user,
            cart=cart,
            total_price=cart.total_price
        )

        # Отправляем email
        order.send_order_email()

        # Устанавливаем статус заказа как 'ordered'
        cart.ordered = True
        cart.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=201)