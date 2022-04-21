from auctions.models import User
from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer class for register function
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user_data = User.objects.create_user(**validated_data)
        user_data.save()
        return user_data


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class for view all user info
    """
    class Meta:
        model = User
        exclude = ['is_superuser', 'is_staff']
        extra_kwargs = {'password': {'write_only': True}}


class UserAuctionResultsSerializer(serializers.ModelSerializer):
    """
    Serializer class for view user login 's auction results
    """
    class Meta:
        model = User
        fields = ['id']
