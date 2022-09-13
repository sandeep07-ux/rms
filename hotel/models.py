from django.db import models
from django.contrib.auth.models import User

# Create your models here.
PROVINCE_CHOICES = (
    ('Biratnagar', 'Biratnagar'),
    ('Janakpur', 'Janakpur'),
    ('Hetauda', 'Hetauda'),
    ('Pokhara', 'Pokhara'),
    ('Butwal', 'Butwal'),
    ('Birendranagar', 'Birendranager'),
    ('Godawari', 'Godawari'),
)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    province = models.CharField(choices=PROVINCE_CHOICES, max_length=50)

    def __str__(self):
        return str(self.id)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='menuimg')

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.item.price


STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel')
)


METHOD = (
    ("Cash On Delivery", "Cash On Delivery"),
    ("Khalti", "Khalti"),
    ("Esewa", "Esewa"),
)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='Pending')
    # payment_method = models.CharField(
    #     max_length=20, choices=METHOD, default="Cash On Delivery")
    # payment_completed = models.BooleanField(
    #     default=False, null=True, blank=True)

    @property
    def total_cost(self):
        return self.quantity * self.item.price
