from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @swagger_auto_schema(
        tags=['Carts'],
        operation_description="Этот эндпоинт позволяет создать новую корзину."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Carts'],
        operation_description="Этот эндпоинт позволяет получить информацию о корзине по ID."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Carts'],
        operation_description="Этот эндпоинт позволяет удалить корзину по ID."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CartItemViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    @swagger_auto_schema(
        tags=['Cart Items'],
        operation_description="Этот эндпоинт позволяет получить список элементов корзины по ID корзины."
    )
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs["cart_pk"])

    @swagger_auto_schema(
        tags=['Cart Items'],
        operation_description="Этот эндпоинт позволяет создать новый элемент корзины."
    )
    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    @swagger_auto_schema(
        tags=['Cart Items'],
        operation_description="Этот эндпоинт позволяет получить контекстный сериализатор для элемента корзины."
    )
    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_pk"]}

    @swagger_auto_schema(
        tags=['Cart Items'],
        operation_description="Этот эндпоинт позволяет создать новый элемент корзины."
    )
    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        cart_id = self.kwargs["cart_pk"]

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            return Response({'error': 'Product already in cart'}, status=status.HTTP_400_BAD_REQUEST)
        except CartItem.DoesNotExist:
            try:
                cart_item = CartItem.objects.create(
                    cart_id=cart_id,
                    product_id=product_id,
                    quantity=quantity,
                    sub_total=0
                )
                serializer = CartItemSerializer(cart_item)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        tags=['Cart Items'],
        operation_description="Этот эндпоинт позволяет обновить элемент корзины."
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        instance = serializer.instance
        new_quantity = serializer.validated_data.get('quantity')

        if new_quantity != instance.quantity:
            instance.quantity = new_quantity
            instance.sub_total = instance.product.price * new_quantity
            instance.save()

        serializer.save()

    @swagger_auto_schema(
        tags=['Cart Items'],
        operation_description="Этот эндпоинт позволяет удалить элемент корзины."
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.quantity > 1:
            instance.quantity -= 1
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
