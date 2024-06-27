from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from .models import Cart, CartItem  # Импортируем модели Cart и CartItem из product.models
from .serializers import CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer
from rest_framework.viewsets import ModelViewSet


class CartViewSet(CreateModelMixin,RetrieveModelMixin,  DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):

    http_method_names = ["get", "post", "patch", "delete"]
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs["cart_pk"])

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer

        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_pk"]}


    def create(self, request, *args, **kwargs):
        # Получаем данные из запроса
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        cart_id = self.kwargs["cart_pk"]

        # Проверяем, существует ли уже такой товар в корзине
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            return Response({'error': 'Product already in cart'}, status=status.HTTP_400_BAD_REQUEST)
        except CartItem.DoesNotExist:
            # Если товара еще нет в корзине, создаем новый элемент корзины
            try:
                cart_item = CartItem.objects.create(
                    cart_id=cart_id,
                    product_id=product_id,
                    quantity=quantity,
                    sub_total=0  # Здесь может быть ваш расчет sub_total, если требуется
                )
                serializer = CartItemSerializer(cart_item)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        # Переопределяем метод update для поддержки вашего логического поведения обновления
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        instance = serializer.instance
        new_quantity = serializer.validated_data.get('quantity')

        # Предположим, что вы хотите обновить количество товара и пересчитать sub_total
        if new_quantity != instance.quantity:
            instance.quantity = new_quantity
            instance.sub_total = instance.product.price * new_quantity  # Пересчет sub_total, если необходимо
            instance.save()

        # Вы также можете добавить другую логику, связанную с обновлением товара в корзине

        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Проверяем, что количество товара в корзине больше 1 перед удалением
        if instance.quantity > 1:
            # Уменьшаем количество на 1
            instance.quantity -= 1
            instance.save()
            # Возвращаем подтверждение об уменьшении количества в корзине
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Если количество товара в корзине равно 1 или меньше, удаляем элемент корзины
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        #Фактическое удаление элемента корзины из базы данных
        instance.delete()

class CartViewSet(CreateModelMixin,RetrieveModelMixin,  DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):

    http_method_names = ["get", "post", "patch", "delete"]
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs["cart_pk"])

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer

        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_pk"]}



