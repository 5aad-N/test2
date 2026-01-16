from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from api.models import Item, Bid
from typing import List


class Command(BaseCommand):
    help = 'Close ended auctions and notify winners'

    def handle(self, *args, **options) -> None:
        """
        Find all active items where end_date has passed,
        determine winner, send email, mark as inactive.
        """
        now = timezone.now()
        ended_items: List[Item] = Item.objects.filter(
            is_active=True,
            end_date__lte=now,
            winner__isnull=True
        )

        self.stdout.write(f"Found {ended_items.count()} ended auctions")

        for item in ended_items:
            # Get highest bid
            highest_bid: Bid | None = item.bids.order_by('-amount').first()

            if highest_bid:
                # Set winner
                item.winner = highest_bid.bidder
                item.save()

                # Send email
                self._send_winner_email(item, highest_bid)

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Closed "{item.title}" - Winner: {highest_bid.bidder.username}'
                    )
                )
            else:
                # No bids, just mark as ended
                item.is_active = False
                item.save()
                self.stdout.write(
                    self.style.WARNING(f'Closed "{item.title}" - No bids')
                )

    def _send_winner_email(self, item: Item, winning_bid: Bid) -> None:
        """Send email to auction winner"""
        subject = f'You won the auction for {item.title}!'

        message = f"""
Congratulations {winning_bid.bidder.username}!

You have won the auction for "{item.title}" with a winning bid of ${winning_bid.amount}.

Item Details:
- Title: {item.title}
- Description: {item.description}
- Your Winning Bid: ${winning_bid.amount}
- Seller: {item.owner.username}
- Seller Email: {item.owner.email}

Please proceed to purchase the item by contacting the seller.

Thank you for using our auction platform!

Best regards,
Auction Team
"""

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[winning_bid.bidder.email],
                fail_silently=False,
            )
            self.stdout.write(
                self.style.SUCCESS(f'Email sent to {winning_bid.bidder.email}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to send email: {str(e)}')
            )
