from rest_framework import serializers
from .models import Product, UserProfile, Purchase, CartItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
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
            'telegram_id',
            'language',
        ]


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = [
            'user',
            'product',
            'purchase_date',
            'receipt',
        ]


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            'user',
            'product',
        ]
