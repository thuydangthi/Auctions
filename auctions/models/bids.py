from django.db import models


class Bids(models.Model):
    price = models.DecimalField(max_digits=6, decimal_places=3)
    created_date = models.DateTimeField(auto_now_add=True)
    auctioneer = models.ForeignKey('User', on_delete=models.ForeignKey, related_name='cards')
    auction = models.ForeignKey('Auctions', on_delete=models.PROTECT, related_name='bid_price')

    class Meta:
        ordering = ['-price']
