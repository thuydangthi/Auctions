from auctions.models import Category
from rest_framework import generics, permissions
from auctions.serializers import CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from permissions import CustomPermissionView


class CategoryList(CustomPermissionView, generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'id': ['exact'],
        'url': ['exact'],
        'auctions': ['exact']
    }
    permission_classes = [permissions.IsAuthenticated]
    permission_classes_by_action = {
        'GET': [permissions.IsAuthenticated],
        'POST': [permissions.IsAdminUser]
    }


class CategoryDetail(CustomPermissionView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]
    permission_classes_by_action = {
        'GET': [permissions.IsAuthenticated]
    }
