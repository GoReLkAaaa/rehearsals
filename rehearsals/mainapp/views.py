from Scripts.bottle import request
from rest_framework import viewsets, permissions
from .models import Product, UserProfile, Purchase, CartItem
from .serializers import ProductSerializer, UserProfileSerializer, PurchaseSerializer, CartItemSerializer
from drf_spectacular.utils import extend_schema_view


@extend_schema_view(tags=['Product'])
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_action_class = {
        'list': ProductSerializer,
        'retrieve': ProductSerializer,
        'create': ProductSerializer,
        'destroy': ProductSerializer,
    }
    permission_classes = [permissions.IsAuthenticated]


    def get_serializer_class(self):
        return self.serializer_action_class.get(self.action, ProductSerializer)


@extend_schema_view(tags=['UserProfile'])
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_action_class = {
        'list': UserProfileSerializer,
        'retrieve': UserProfileSerializer,
        'create': UserProfileSerializer,
        'destroy': UserProfileSerializer,
    }
    permission_classes = [permissions.IsAuthenticated]


    def get_serializer_class(self):
        return self.serializer_action_class.get(self.action, UserProfileSerializer)


    def get_queryset(self):
        telegram_id = self.request.query_params.get('telegram_id')
        if telegram_id:
            return UserProfile.objects.filter(telegram_id=telegram_id)
        return super().get_queryset()


@extend_schema_view(tags=['Purchase'])
class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_action_class = {
        'list': PurchaseSerializer,
        'retrieve': PurchaseSerializer,
        'create': PurchaseSerializer,
        'destroy': PurchaseSerializer,
    }
    permission_classes = [permissions.IsAuthenticated]


    def get_serializer_class(self):
        return self.serializer_action_class.get(self.action, PurchaseSerializer)


@extend_schema_view(tags=['CartItem'])
class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_action_class = {
        'list': CartItemSerializer,
        'retrieve': CartItemSerializer,
        'create': CartItemSerializer,
        'destroy': CartItemSerializer,
    }
    permission_classes = [permissions.IsAuthenticated]


    def get_serializer_class(self):
        return self.serializer_action_class.get(self.action, CartItemSerializer)


    def get_queryset(self):
        telegram_id = self.request.query_params.get('telegram_id')
        if telegram_id:
            try:
                profile = UserProfile.objects.get(telegram_id=telegram_id)
                return CartItem.objects.filter(user=profile)
            except UserProfile.DoesNotExist:
                return CartItem.objects.none()
        return CartItem.objects.all()


    def perform_create(self, serializer):
        serializer.save(user=self.request.user.profile)