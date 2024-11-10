from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Cart, CartItem, Order, PaymentMethod
from product.models import Product
from .serializers import CartItemsSerializer, OrderSerializer

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['cart'],
        operation_description="Получить список товаров в корзине пользователя.",
        responses={
            200: openapi.Response(
                description="Список товаров в корзине пользователя",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID товара"),
                            'name': openapi.Schema(type=openapi.TYPE_STRING, description="Название товара"),
                            'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description="Количество товара"),
                            'price': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description="Цена товара"),
                            'description': openapi.Schema(type=openapi.TYPE_STRING, description="Описание товара"),
                            'image_url': openapi.Schema(type=openapi.TYPE_STRING, description="URL изображения товара"),
                        },
                    ),
                ),
            ),
            404: openapi.Response(
                description="Корзина не найдена",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}
                )
            ),
        },
    )
    def get(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user, ordered=False).first()

        if not cart:
            return Response({'error': 'Cart not found'}, status=404)

        queryset = CartItem.objects.filter(cart=cart)
        serializer = CartItemsSerializer(queryset, many=True)

        # Расчет общей стоимости корзины
        total_price = sum(item.price * item.quantity for item in queryset)

        return Response({
            'items': serializer.data,
            'total_quantity': sum(item.quantity for item in queryset),
            'subtotal': total_price,
            'totalPrice': total_price,
        })

    @swagger_auto_schema(
        tags=['cart'],
        operation_description="Добавить товар в корзину.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID товара"),
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description="Количество товара"),
            },
            required=['product', 'quantity']
        ),
        responses={
            201: openapi.Response(
                description="Товар добавлен в корзину",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={'success': openapi.Schema(type=openapi.TYPE_STRING)}
                )
            ),
            400: openapi.Response(
                description="Ошибка при добавлении товара",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}
                )
            ),
        }
    )
    def post(self, request):
        data = request.data
        user = request.user
        # Получаем корзину пользователя (или создаем новую, если она не существует)
        cart, _ = Cart.objects.get_or_create(user=user, ordered=False)

        # Получаем товар, который был добавлен
        product = get_object_or_404(Product, id=data.get('product'))
        quantity = int(data.get('quantity', 1))

        # Проверка на корректность количества
        if quantity <= 0:
            return Response({'error': 'Quantity must be greater than 0'}, status=400)

        if quantity > product.quantity:
            return Response({'error': 'Not enough stock available'}, status=400)

        # Рассчитываем цену с учетом промоакции (если она есть)
        price = product.price
        promotion = product.promotion or 0
        if promotion > 0:
            price *= (1 - promotion / 100)

        # Добавляем товар в корзину без уменьшения количества на складе
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'price': price, 'quantity': quantity, 'user': user}
        )

        if not created:
            # Обновляем существующий CartItem
            cart_item.quantity += quantity
            cart_item.price = price * cart_item.quantity
            cart_item.save()

        # Обновляем общую стоимость корзины
        cart.total_price = sum(item.price * item.quantity for item in CartItem.objects.filter(cart=cart))
        cart.save()

        return Response({'success': 'Item added to your cart'})

    def put(self, request):
        cart_item = get_object_or_404(CartItem, id=request.data.get('id'))
        new_quantity = int(request.data.get('quantity', 1))

        if new_quantity <= 0:
            return Response({'error': 'Invalid quantity'}, status=400)

        if new_quantity > cart_item.product.quantity:
            return Response({'error': 'Not enough stock'}, status=400)

        product = cart_item.product
        price = product.price * (1 - (product.promotion or 0) / 100)

        cart_item.product.quantity += cart_item.quantity - new_quantity
        cart_item.quantity = new_quantity
        cart_item.price = price * new_quantity
        cart_item.save()
        product.save()

        cart_item.cart.total_price = sum(item.price * item.quantity for item in cart_item.cart.items.all())
        cart_item.cart.save()

        return Response({'success': 'Product updated'})

    @swagger_auto_schema(
        tags=['cart'],
        operation_description="Удалить товар из корзины.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID товара")},
            required=['id']
        ),
        responses={
            204: openapi.Response(description="Товар удалён"),
            404: openapi.Response(description="Товар не найден")
        }
    )
    def delete(self, request):
        # Получаем id продукта из запроса
        product_id = request.data.get('id')
        if not product_id:
            return Response({'error': 'Product ID not provided'}, status=400)

        # Получаем все CartItem для данного продукта и проверяем, что они принадлежат текущему пользователю
        cart_items = CartItem.objects.filter(product__id=product_id, user=request.user)

        if not cart_items.exists():
            return Response({'error': 'No CartItem found for this product in your cart'}, status=404)

        for cart_item in cart_items:
            # Возвращаем количество товара обратно на склад
            cart_item.product.quantity += cart_item.quantity
            cart_item.product.save()

            # Удаляем товар из корзины
            cart = cart_item.cart
            cart_item.delete()

            # Обновляем общую цену корзины
            cart.total_price = sum(item.price * item.quantity for item in cart.items.all())
            cart.save()

        return Response({'success': 'Items removed from cart'}, status=204)


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['order'],
        operation_description="Оформить заказ. Введите адрес и способ оплаты: 1 - наличные, 2 - карта.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'address': openapi.Schema(type=openapi.TYPE_STRING, description="Адрес доставки"),
                'payment_method': openapi.Schema(type=openapi.TYPE_INTEGER, description="Способ оплаты (1 - наличные, 2 - карта)")
            },
            required=['address', 'payment_method']
        ),
        responses={
            201: openapi.Response(description="Заказ создан"),
            400: openapi.Response(description="Ошибка создания заказа")
        }
    )
    def post(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user, ordered=False).first()

        if not cart:
            return Response({'error': 'Cart not found'}, status=400)

        # Уменьшаем количество товара на складе при оформлении заказа
        for cart_item in cart.cartitem_set.all():
            product = cart_item.product
            product.quantity -= cart_item.quantity
            product.save()

        # Создаем заказ
        payment_method = get_object_or_404(PaymentMethod, id=request.data['payment_method'])
        order = Order.objects.create(
            user=user,
            total_price=cart.total_price,
            address=request.data['address'],
            payment_method=payment_method
        )

        cart.ordered = True
        cart.save()

        return Response(OrderSerializer(order).data, status=201)
