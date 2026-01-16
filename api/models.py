from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.utils import timezone

# Create your models here.


class User(AbstractUser):
    """Custom user model with additional profile fields."""

    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('JPY', 'Japanese Yen'),
        ('AUD', 'Australian Dollar'),
    ]

    email: str = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(
        upload_to="profile_pics/",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],
    )
    currency_preference: str = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='USD',
    )

    @property
    def bid_item_ids(self) -> list[int]:
        """Returns unique IDs of bids this user has made"""
        return list(self.bids.values_list("item_id", flat=True).distinct())

    @property
    def questioned_item_ids(self) -> list[int]:
        """Returns unique IDs of items this user has asked questions about"""
        return list(self.questions_asked.values_list("item_id", flat=True).distinct())

    def __str__(self) -> str:
        return f"{self.username} ({self.email})"


class Item(models.Model):
    """Auction item/listing"""

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")
    title: str = models.CharField(max_length=200)
    description: str = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(
        upload_to="item_pics/",
        validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],
    )
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active: bool = models.BooleanField(default=True)
    winner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="won_items"
    )

    def __str__(self) -> str:
        return f"{self.title} by {self.owner.username}"

    @property
    def is_ended(self) -> bool:
        """Return True if auction has ended (current time >= end_date)."""
        return timezone.now() >= self.end_date

    @property
    def bid_count(self) -> int:
        """Return total number of bids placed on this item."""
        return self.bids.count()


class Bid(models.Model):
    """Bid on an auction item"""

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"${self.amount} on {self.item.title} by {self.bidder.username}"


class Question(models.Model):
    """Q&A about items"""

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="questions")
    asker = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="questions_asked"
    )
    question_text: str = models.TextField()
    answer_text: str = models.TextField(blank=True, default="")
    asked_at = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_answered(self) -> bool:
        """Return True if the question has been answered."""
        return bool(self.answer_text)

    def __str__(self) -> str:
        return f"Q on {self.item.title} by {self.asker.username}"
