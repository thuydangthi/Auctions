from auctions.models.category import Category
from auctions.models import Auctions, AuctionsImages
from rest_framework import serializers
import datetime
from .auction_images import AuctionsImagesSerializer


def positive_number(value, field_name):
    if value <= 0:
        raise serializers.ValidationError(f'{field_name} must be positive.')


class AuctionOverviewSerializer(serializers.ModelSerializer):
    """
    Serializer class of get list auction api
    """
    images = AuctionsImagesSerializer(many=True, required=False)
    seller__str = serializers.SerializerMethodField()
    left_time = serializers.SerializerMethodField()
    sum_of_bids = serializers.SerializerMethodField()
    sum_of_follower = serializers.SerializerMethodField()
    is_auction_allowed = serializers.SerializerMethodField()

    class Meta:
        model = Auctions
        exclude = ('description',  'created_date', 'deleted_at')
        extra_kwargs = {'quantity': {'min_value': 1},
                        'seller': {'read_only': True}}

    def get_left_time(self, obj):
        return obj.get_left_time()

    def get_sum_of_bids(self, obj):
        return obj.sum_of_bids()

    def get_sum_of_follower(self, obj):
        return obj.sum_of_follower()

    def get_seller__str(self, obj):
        return obj.seller.__str__()

    def get_is_auction_allowed(self, obj):
        return obj.is_auction_allowed()


class AuctionSerializer(serializers.ModelSerializer):
    """
    Serializer class of auction api
    """
    images = AuctionsImagesSerializer(many=True, required=False)
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True)
    left_time = serializers.SerializerMethodField()
    seller__str = serializers.SerializerMethodField()
    is_auction_allowed = serializers.SerializerMethodField()
    total_number_of_bids = serializers.SerializerMethodField()
    sum_of_bids = serializers.SerializerMethodField()
    sum_of_follower = serializers.SerializerMethodField()
    current_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Auctions
        fields = '__all__'
        extra_kwargs = {'quantity': {'min_value': 1},
                        'seller': {'read_only': True}}

    def get_left_time(self, obj):
        return obj.get_left_time()

    def get_current_quantity(self, obj):
        return obj.get_current_quantity()

    def get_sum_of_bids(self, obj):
        return obj.sum_of_bids()

    def get_sum_of_follower(self, obj):
        return obj.sum_of_follower()

    def validate_start_time(self, value):
        if value < datetime.datetime.now():
            raise serializers.ValidationError(
                "Start time must be greater than now.")
        return value

    def get_seller__str(self, obj):
        return obj.seller.__str__()

    def get_is_auction_allowed(self, obj):
        return obj.is_auction_allowed()

    def get_total_number_of_bids(self, obj):
        return obj.total_number_of_bids()

    def validate_min_price(self, value):
        positive_number(value, 'Minimum Auction')
        return value

    def validate_ready_to_sell_price(self, value):
        positive_number(value, 'Ready-to-sell price')
        return value

    def validate(self, data):
        min_price = data.get('min_price', None)
        ready_to_sell_price = data.get('ready_to_sell_price', None)
        if min_price and ready_to_sell_price and min_price > ready_to_sell_price:
            raise serializers.ValidationError({
                'ready_to_sell_price': ['Ready-to-sell price must be greater than or equal minimum Auction.'],
            })

        start_time = data.get('start_time', None)
        end_time = data.get('end_time', None)
        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError({
                'end_time': ['End time must be greater than start time.'],
            })
        return data

    def create(self, validated_data):
        categories = validated_data.pop('categories')
        images_data = validated_data.pop('images')
        auction = Auctions.objects.create(**validated_data)
        for image in images_data:
            AuctionsImages.objects.create(auction=auction, **image)
        for category in categories:
            auction.categories.add(category)
        return auction
