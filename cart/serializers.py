from rest_framework import serializers
from .models import Cart, CartItem  # Импортируем Cart и CartItem из текущего приложения
from product.serializers import ProductSerializer
from product.models import Product

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "price"]

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many=False)
    sub_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "cart", "product", "quantity", "sub_total"]

    def get_sub_total(self, cartitem):
        return cartitem.quantity * cartitem.product.price


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("not found")

        return value

    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]

        try:
            cartitem = CartItem.objects.get(product_id=product_id, cart_id=cart_id)
            cartitem.quantity += quantity
            cartitem.save()

            self.instance = cartitem

        except:

           self.instance = CartItem.objects.create(cart_id=cart_id **self.validated_data)

        return self.instance
    class Meta:
        model = CartItem
        fields = ["id", "product_id", "quantity"]

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    main_total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "items", "main_total"]

    def get_main_total(self, cart):
        total = 0
        for item in cart.items.all():
            total += item.quantity * item.product.price
        return total
