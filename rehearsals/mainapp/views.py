from rest_framework import viewsets, permissions
from drf_spectacular.utils import extend_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import TelegramTokenObtainPairSerializer
from .models import Product, UserProfile, Purchase, CartItem
from .serializers import ProductSerializer, UserProfileSerializer, PurchaseSerializer, CartItemSerializer, CartItemCreateSerializer


class TelegramTokenObtainPairView(TokenObtainPairView):
    serializer_class = TelegramTokenObtainPairSerializer


@extend_schema_view(tags=['Product'])
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_action_class = {
        'list': ProductSerializer,
        'retrieve': ProductSerializer,
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
    queryset = CartItem.objects.select_related('user', 'product').all()
    serializer_action_class = {
        'list': CartItemSerializer,
        'retrieve': CartItemSerializer,
        'create': CartItemSerializer,
        'destroy': CartItemSerializer,
    }

    permission_classes = [permissions.IsAuthenticated]


    def get_serializer_class(self):
        return self.serializer_action_class.get(self.action, CartItemSerializer)


    def get_serializer_class(self):
        if self.action == 'create':
            return CartItemCreateSerializer
        return CartItemSerializer

    def get_queryset(self):
        tg_id = self.request.query_params.get('telegram_id')
        if tg_id:
            return self.queryset.filter(user__telegram_id=tg_id)
        return self.queryset