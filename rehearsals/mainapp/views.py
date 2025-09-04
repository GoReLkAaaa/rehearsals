from rest_framework import viewsets, permissions
from .models import Product, UserProfile, Purchase, CartItem
from .serializers import ProductSerializer, UserProfileSerializer, PurchaseSerializer, CartItemSerializer
from drf_spectacular.utils import extend_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import TelegramTokenObtainPairSerializer


class TelegramTokenObtainPairView(TokenObtainPairView):
    serializer_class = TelegramTokenObtainPairSerializer


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


    def perform_create(self, serializer):
        serializer.save(user=self.request.user.profile)