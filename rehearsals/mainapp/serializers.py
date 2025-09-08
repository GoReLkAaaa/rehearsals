from rest_framework import serializers
from .models import Product, UserProfile, Purchase, CartItem
from rest_framework_simplejwt.tokens import RefreshToken


class TelegramTokenObtainPairSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        telegram_id = attrs.get("telegram_id")

        try:
            user = UserProfile.objects.get(telegram_id=telegram_id)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким Telegram ID не найден")

        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


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


class CartItemCreateSerializer(serializers.ModelSerializer):

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True,
    )

    telegram_id = serializers.IntegerField(write_only=True)
    product = ProductSerializer(read_only=True)


    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'telegram_id']


    def validate(self, attrs):
        tg_id = attrs.get('telegram_id')

        try:
            user = UserProfile.objects.get(telegram_id=tg_id)

        except UserProfile.DoesNotExist:
            raise serializers.ValidationError({'telegram_id': 'Пользователь с таким Telegram ID не найден'})

        attrs['user'] = user

        return attrs


    def create(self, validated_data):
        validated_data.pop('telegram_id', None)
        user = validated_data['user']
        product = validated_data['product']

        obj, created = CartItem.objects.get_or_create(user=user, product=product)

        return obj