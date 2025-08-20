from rest_framework import serializers
from .models import Product, CartItem, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    # def create(self, validated_data):
    #     password = validated_data["passowrd"]
    #     hashPass = "hashedpassword"
    #     validated_data["password"] = hashPass
    #     return Product.objects.create(validated_data)
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    class Meta:
        model = OrderItem
        fields = ['product', 'product_name', 'quantity', 'price_at_purchase', 'subtotal']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = '__all__'