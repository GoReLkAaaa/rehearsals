from rest_framework import serializers
from .models import Product, UserProfile, Purchase, CartItem
from rest_framework_simplejwt.tokens import RefreshToken


class TelegramTokenObtainPairSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField()


    username = None
    password = None

    def validate(self, attrs):
        telegram_id = attrs.get("telegram_id")


        try:
            user_profile = UserProfile.objects.get(telegram_id=telegram_id)
            user = user_profile.user
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError("User with this telegram_id not found")

        if not user.is_active:
            raise serializers.ValidationError("User is inactive")


        refresh = RefreshToken.for_user(user)

        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return data


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
