from rest_framework import serializers
from .models import Cart, CartItem
from product.serializers import ProductSerializer
from users.models import User

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartItemsSerializer(serializers.ModelSerializer):
    cart = CartSerializer()
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = '__all__'

    def to_representation(self, instance):

        representation = super().to_representation(instance)


        if 'cart' in representation and 'user' in representation['cart']:
            user_id = representation['cart']['user']
            if isinstance(user_id, int):
                try:
                    user = User.objects.get(id=user_id)
                    representation['cart']['user'] = user.first_name
                except User.DoesNotExist:
                    representation['cart']['user'] = 'unknown'


        if 'user' in representation:
            user_id = representation['user']
            if isinstance(user_id, int):
                try:
                    user = User.objects.get(id=user_id)
                    representation['user'] = user.first_name
                except User.DoesNotExist:
                    representation['user'] = 'unknown'

        return representation
