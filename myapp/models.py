from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Profile(models.Model):
    ROLE_CHOICES = (
        ("farmer", "Farmer / producer"),
        ("buyer", "Buyer"),
        ("driver", "Driver / logistics partner"),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=30)
    county = models.CharField(max_length=80)
    bio = models.TextField(blank=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"


class Product(models.Model):
    CATEGORY_CHOICES = (
        ("vegetables", "Vegetables"),
        ("fruit", "Fruit"),
        ("grains", "Grains"),
        ("dairy", "Dairy & eggs"),
        ("other", "Other"),
    )
    farmer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    county = models.CharField(max_length=80)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quantity_kg = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    minimum_order_kg = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    available_from = models.DateField(null=True, blank=True)
    image_url = models.URLField(blank=True)
    organic = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def average_rating(self):
        value = self.reviews.aggregate(models.Avg("rating"))["rating__avg"]
        return round(value, 1) if value else None

    def __str__(self):
        return self.name


class DriverProfile(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="driver")
    vehicle_type = models.CharField(max_length=80)
    capacity_kg = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    completed_deliveries = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.profile.user.get_full_name() or self.profile.user.username


class Order(models.Model):
    STATUS_CHOICES = (
        ("processing", "Processing"),
        ("transit", "In transit"),
        ("complete", "Complete"),
        ("cancelled", "Cancelled"),
    )
    buyer = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="orders")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="orders")
    driver = models.ForeignKey(DriverProfile, on_delete=models.PROTECT, related_name="orders", null=True, blank=True)
    quantity_kg = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="processing")
    payment_secured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        return self.quantity_kg * self.unit_price


class Review(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="reviews_written")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews", null=True, blank=True)
    driver = models.ForeignKey(DriverProfile, on_delete=models.CASCADE, related_name="reviews", null=True, blank=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(rating__lte=5), name="review_rating_1_to_5"),
        ]
