from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    starting_price = models.IntegerField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    image=models.ImageField(upload_to='media/', blank=True)
    current_price = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        if self.bids.all() != []:
            return f"{self.title}: ${self.current_price} [Listed by: {self.seller}]"
    def save(self, *args, **kwargs):
        if self.current_price == None:
            self.current_price = self.starting_price
        super(Listing, self).save(*args, **kwargs)


class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="watchlist")
    listings = models.ManyToManyField(Listing, blank=True)

    def __str__(self):
        return f"{self.user}\'s Watchlist [{len(self.listings.all())} listing(s)]"

class Category(models.Model):
    category = models.CharField(max_length=20)
    listings = models.ManyToManyField(Listing, related_name="categories", blank=True)

    def __str__(self):
        return f"{self.category}"

    class Meta:
        verbose_name_plural = "categories"

class Bid(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidded_on")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid = models.IntegerField()

    def __str__(self):
        return f"{self.buyer.username} bids ${self.bid} on {self.listing.title}"

class Comment(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    time = models.DateTimeField()

    def __str__(self):
        return f"{self.user}\'s comment on {self.listing.title}"