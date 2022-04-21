from permissions import CustomPermissionView
from auctions.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from auctions.serializers import UserSerializer, UserRegisterSerializer
from auctions.permissions import UserOrAdminPermissions
from django.shortcuts import get_object_or_404


class UserRegisterList(CustomPermissionView, APIView):
    """
    List all user, or create a new user.
    """
    permission_classes = [IsAuthenticated]
    permission_classes_by_action = {
        'GET': [IsAuthenticated],
        'POST': [AllowAny]
    }

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(CustomPermissionView, APIView):
    """
    Retrieve, update or delete a user instance.
    """

    permission_classes = [IsAuthenticated]
    permission_classes_by_action = {
        'DELETE': [IsAdminUser],
        'PATCH': [UserOrAdminPermissions]
    }

    def get_object(self, pk):
        data = get_object_or_404(User, id=pk)
        self.check_object_permissions(self.request, data)
        return data

    def get(self, request, pk, format=None):
        user_data = self.get_object(pk)
        serializer = UserSerializer(user_data)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        user_data = self.get_object(pk)
        serializer = UserSerializer(user_data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user_data = self.get_object(pk)
        user_data.delete()
        return Response({"detail": "Delete user successfully!"}, status=status.HTTP_204_NO_CONTENT)
