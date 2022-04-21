from django.db import models


class Watchlist(models.Model):
    auction = models.ForeignKey(
        'Auctions', on_delete=models.PROTECT, related_name='tracking_list')
    created_date = models.DateTimeField(auto_now_add=True)
    deleted_date = models.DateTimeField(null=True)
    follower = models.ForeignKey('User', on_delete=models.CASCADE)

    def owner(self):
        return self.follower
