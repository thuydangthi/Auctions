from auctions.models import Bids
from rest_framework import serializers


class BidsSerializer(serializers.ModelSerializer):
    """
    Serializer class of Bids api
    """
    auctioneer = serializers.ReadOnlyField(source='auctioneer.id')
    auctioneer_name = serializers.SerializerMethodField()

    class Meta:
        model = Bids
        fields = '__all__'
        extra_kwargs = {'auctioneer': {'read_only': True}}

    def get_auctioneer_name(self, obj):
        return obj.auctioneer.hidden_name()

    def validate(self, data):
        price = data.get('price', None)
        auction = data.get('auction', None)
        if auction:
            if auction.get_current_quantity() <= 0:
                raise serializers.ValidationError({
                    'auction': ['The auction is sold out.'],
                })
            if not auction.is_auction_allowed():
                raise serializers.ValidationError({
                    'auction': ['This auction was expired or not due or has been disabled.'],
                })
            if price < auction.min_price:
                raise serializers.ValidationError({
                    'auction': ['The bid amount must be greater than or equal the minimum bid price.'],
                })
            max_price = auction.max_bid()
            if max_price and price <= max_price:
                raise serializers.ValidationError({
                    'auction': ['This bid has been auctioned, please choose a higher price.'],
                })
        return data
