from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.core.validators import RegexValidator


# Create your models here.
class Customerdetails(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    locality = models.CharField(max_length=150, verbose_name="Nearest Location")
    city = models.CharField(max_length=150, verbose_name="City")
    email = models.EmailField(null=True)
    mobno = models.CharField(null=True, max_length=10, validators=[RegexValidator(r'^\d{3}-\d{3}-\d{4}$')])
    rationcardno = models.PositiveIntegerField()
    rationcardphoto = models.ImageField(upload_to='media/images', null=True)

    def __str__(self):
        return self.locality


class Category(models.Model):
    status_choices = [
        ('Subseedy', 'Subseedy'),
        ('Nosubseedy', 'Nosubseedy'),
    ]
    title = models.CharField(max_length=50, verbose_name="Category Title")
    slug = models.SlugField(max_length=55, verbose_name="Category Slug")
    description = models.TextField(blank=True, verbose_name="Category Description")
    category_image = models.ImageField(upload_to='media/category', blank=True, null=True, verbose_name="Category Image")
    is_active = models.BooleanField(verbose_name="Is Active?")
    is_featured = models.BooleanField(verbose_name="Is Featured?")
    choice = models.CharField(max_length=40, choices=status_choices)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name="Product Title")
    slug = models.SlugField(max_length=160, verbose_name="Product Slug")
    sku = models.CharField(max_length=255, unique=True, verbose_name="Unique Product ID (SKU)")
    short_description = models.TextField(verbose_name="Short Description")
    detail_description = models.TextField(blank=True, null=True, verbose_name="Detail Description")
    product_image = models.ImageField(upload_to='media/product', blank=True, null=True, verbose_name="Product Image")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    productStock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, verbose_name="Product Categoy", on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name="Is Active?")
    is_featured = models.BooleanField(verbose_name="Is Featured?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    def __str__(self):
        return str(self.user)

    # Creating Model Property to calculate Quantity x Price
    @property
    def total_price(self):
        return self.quantity * self.product.price


STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled')
)


class Order(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)

    order_id = models.CharField(null=True, max_length=50)
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE, null=True)
    total = models.FloatField(null=True)
    subtotal = models.FloatField(null=True)
    gst = models.IntegerField(null=True)
    address = models.ForeignKey(Customerdetails, verbose_name="Shipping Address", on_delete=models.CASCADE, null=True)
    ordered_date = models.DateTimeField(default=datetime.now, blank=True, verbose_name="Ordered Date")
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=50,
        default="pending"
    )


class Orderdetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    product = models.CharField(null=True, max_length=50)
    product_name = models.CharField(null=True, max_length=50)
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    price = models.FloatField()


class staff(models.Model):
    name = models.CharField(max_length=250)
    staff_id = models.PositiveIntegerField()
    password = models.PositiveIntegerField()


class payments(models.Model):
    name = models.CharField(max_length=250)
    cardno = models.PositiveIntegerField()

    amount = models.PositiveIntegerField()


class DailyReport(models.Model):
    category = models.ForeignKey(Category, verbose_name="Product Categoy", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class stock(models.Model):
    category = models.ForeignKey(Category, verbose_name="Product Categoy", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()
    date = models.CharField(max_length=250)
    image = models.ImageField(upload_to="media/images", null=True)

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="{}" width="250" height="250" />'.format(self.image.url))
        else:
            return 'No Image Found'

    image_tag.short_description = 'image preview'
    image_tag.allow_tags = True


class Feedback(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
    msg = models.TextField()


class contact(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
    mobno = models.CharField(null=True, max_length=10, validators=[RegexValidator(r'^\d{3}-\d{3}-\d{4}$')])
    message = models.TextField()


class Adds(models.Model):
    add = models.ImageField(upload_to='media/addimage')


RATING = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    review_text = models.TextField()
    review_rating = models.IntegerField(choices=RATING, null=True)

    class Meta:
        verbose_name_plural = 'Reviews'

    def get_review_rating(self):
        return self.review_rating
