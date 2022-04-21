from auctions.models import Watchlist, Auctions
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status


class WatchlistSerializer(serializers.ModelSerializer):
    """
    Serializer class of Watchlist api
    """
    auction = serializers.PrimaryKeyRelatedField(
        queryset=Auctions.objects.filter(deleted_at__isnull=True), required=True)

    class Meta:
        model = Watchlist
        fields = '__all__'
        extra_kwargs = {'follower': {'read_only': True}}

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['follower_name'] = instance.follower.__str__()
        return response

    def validate(self, data):
        user = self.context['request'].user
        auction = data['auction']
        if auction.seller_id == user.id:
            raise serializers.ValidationError({
                'auction': ["You don't have permission."],
            })
        if Watchlist.objects.filter(auction=auction, follower=user, deleted_date__isnull=True).exists():
            raise serializers.ValidationError({
                'auction': ['You have followed this auction.'],
            })

        return data
