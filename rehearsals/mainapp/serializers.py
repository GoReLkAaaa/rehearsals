from rest_framework import serializers
from .models import Product, UserProfile, Purchase, CartItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name_ru',
            'name_uz',
            'category',
            'description_ru',
            'description_uz',
            'image',
            'video',
            'recipe_text',
            'recipe_text_uz',
            'price',
            'recipe_image',
            'recipe_video',
            'recipe_file',
            'recipe_source_link',
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id',
            'telegram_id',
            'language',
        ]


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = [
            'id',
            'user',
            'product',
            'purchase_date',
            'receipt',
        ]


class CartItemSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True,
    )

    class Meta:
        model = CartItem
        fields = [
            'id',
            'user',
            'product',
            'product_id'
        ]
        read_only_fields = ['user']
