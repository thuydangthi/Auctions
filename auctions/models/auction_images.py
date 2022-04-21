from django.db import models


class AuctionsImages(models.Model):
    image = models.TextField()
    auction = models.ForeignKey('Auctions', on_delete=models.PROTECT, related_name='images')

    def owner(self):
        return self.auction.seller