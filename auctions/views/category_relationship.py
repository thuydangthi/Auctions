from auctions.models import CategoryRelationship
from rest_framework import generics, permissions
from auctions.serializers import CategoryRelationshipSerializer
from auctions.permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from permissions import CustomPermissionView


class CategoryRelationshipList(CustomPermissionView, generics.ListCreateAPIView):
    queryset = CategoryRelationship.objects.all()
    serializer_class = CategoryRelationshipSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
    }
    permission_classes = [permissions.IsAuthenticated]
    permission_classes_by_action = {
        'GET': [permissions.IsAuthenticated],
        'POST': [permissions.IsAdminUser]
    }


class CategoryRelationshipDetail(CustomPermissionView, generics.RetrieveUpdateDestroyAPIView):
    queryset = CategoryRelationship.objects.all()
    serializer_class = CategoryRelationshipSerializer
    permission_classes = [permissions.IsAdminUser]
    permission_classes_by_action = {
        'GET': [permissions.IsAuthenticated]
    }
