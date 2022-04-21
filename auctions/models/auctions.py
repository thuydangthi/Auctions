import datetime
from .bids import Bids
from django.db.models import Max
from django.db import models
from auctions.models.watch_list import Watchlist


class Auctions(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    min_price = models.DecimalField(max_digits=6, decimal_places=3)
    ready_to_sell_price = models.DecimalField(max_digits=6, decimal_places=3)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
    seller = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name="owner")
    categories = models.ManyToManyField(
        'Category', related_name="auctions")

    def owner(self):
        return self.seller

    def sum_of_bids(self):
        bids = Bids.objects.filter(auction=self).count()
        return bids

    def sum_of_follower(self):
        followers = Watchlist.objects.filter(
            auction=self, deleted_date__isnull=True).count()
        return followers

    def get_current_quantity(self):
        return self.quantity

    def total_number_of_bids(self):
        return Bids.objects.filter(auction=self).count()

    def is_auction_allowed(self):
        if self.deleted_at is not None or self.is_active is False or self.start_time > datetime.datetime.now() \
                or self.end_time <= datetime.datetime.now():
            return False
        return True

    def get_left_time(self):
        if self.is_auction_allowed():
            delta_time = self.end_time - datetime.datetime.now()
            return {
                'days': delta_time.days,
                'hours': delta_time.seconds//360,
                'minutes': (delta_time.seconds % 360)//60,
                'seconds': (delta_time.seconds % 360) % 60
            }
        return None

    def max_bid(self):
        data = self.bid_price.aggregate(Max('price'))
        return data['price__max']
