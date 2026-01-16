from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import Item, Bid, Question
from datetime import timedelta
from django.utils import timezone
from decimal import Decimal
from django.core.files.base import ContentFile
import io
from PIL import Image

User = get_user_model()


class Command(BaseCommand):
    help = 'Create test data for auction app'

    def handle(self, *args, **options) -> None:
        self.stdout.write("Creating test users...")

        # Create 5 test users
        users = []
        for i in range(1, 6):
            username = f'testuser{i}'
            email = f'testuser{i}@example.com'

            # Check if user exists
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                self.stdout.write(f"User {username} already exists")
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='testpass123',
                    date_of_birth='1990-01-01',
                )
                self.stdout.write(self.style.SUCCESS(f"Created user: {username}"))

            users.append(user)

        self.stdout.write("Creating test auction items...")

        # Item data
        items_data = [
            ("Vintage Bicycle", "Classic red bicycle in excellent condition", "150.00"),
            ("Gaming Laptop", "High-performance laptop with RTX graphics", "800.00"),
            ("Antique Watch", "Rare pocket watch from the 1950s", "300.00"),
            ("Designer Handbag", "Authentic leather handbag", "250.00"),
            ("Camera Equipment", "Professional DSLR camera with lenses", "600.00"),
            ("Vintage Vinyl Records", "Collection of 50+ classic albums", "120.00"),
            ("Smart Home Hub", "Latest model with voice control", "80.00"),
            ("Art Painting", "Original oil painting by local artist", "400.00"),
            ("Leather Jacket", "Genuine leather motorcycle jacket", "180.00"),
            ("Kitchen Appliances", "Food processor and blender set", "90.00"),
        ]

        for i, (title, description, price) in enumerate(items_data):
            # Create simple colored image
            img = Image.new('RGB', (400, 300), color=(100 + i*10, 150, 200 - i*5))
            img_io = io.BytesIO()
            img.save(img_io, format='JPEG')
            img_file = ContentFile(img_io.getvalue(), name=f'item{i+1}.jpg')

            # Vary end dates
            days_ahead = (i % 5) + 1  # 1-5 days
            end_date = timezone.now() + timedelta(days=days_ahead)

            item = Item.objects.create(
                owner=users[i % 5],
                title=title,
                description=description,
                starting_price=Decimal(price),
                current_price=Decimal(price),
                picture=img_file,
                end_date=end_date,
            )

            # Add some bids
            if i % 2 == 0:  # Add bids to half the items
                bid_amount = Decimal(price) + Decimal('10.00')
                Bid.objects.create(
                    item=item,
                    bidder=users[(i + 1) % 5],
                    amount=bid_amount,
                )
                item.current_price = bid_amount
                item.save()

            # Add some questions
            if i % 3 == 0:  # Add questions to 1/3 of items
                q = Question.objects.create(
                    item=item,
                    asker=users[(i + 2) % 5],
                    question_text="What is the condition of this item?",
                )
                # Answer some questions
                if i % 6 == 0:
                    q.answer_text = "The item is in excellent condition with no defects."
                    q.answered_at = timezone.now()
                    q.save()

            self.stdout.write(self.style.SUCCESS(f"Created item: {title}"))

        self.stdout.write(self.style.SUCCESS("\nTest data created successfully!"))
        self.stdout.write("\nTest user credentials:")
        self.stdout.write("Username: testuser1-5")
        self.stdout.write("Password: testpass123")
