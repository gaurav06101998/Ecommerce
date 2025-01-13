from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)  # For featured products
    sales = models.PositiveIntegerField(default=0)  # Track the number of sales for best-selling
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Discount on the product

    def __str__(self):
        return self.name

    def update_stock(self, quantity):
        """ Update stock after a purchase or cart operation. """
        if quantity <= self.stock:
            self.stock -= quantity
            self.save()  # Save the updated stock
        else:
            raise ValueError("Not enough stock available.")

    def get_discounted_price(self, discount=0):
        """ Return the price after applying the discount. """
        return self.price - (self.price * discount / 100)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def get_total_price(self):
        """ Calculate total price of all items in the cart """
        return sum(item.get_subtotal() for item in self.cart_items.all())

    def is_empty(self):
        """ Check if the cart is empty """
        return self.cart_items.count() == 0


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')  # Prevent duplicates of the same product in the cart.

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_subtotal(self):
        """ Calculate the subtotal for this cart item """
        return self.product.price * self.quantity

    def update_quantity(self, quantity):
        """ Update the quantity of a cart item """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")
        self.quantity = quantity
        self.save()


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipped = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    def get_total_price(self):
        """ Calculate the total price for the entire order (from the cart) """
        return self.cart.get_total_price()

    def mark_as_shipped(self):
        """ Mark the order as shipped """
        self.status = 'shipped'
        self.shipped = True
        self.save()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

    def has_avatar(self):
        """ Check if the user has set an avatar """
        return bool(self.avatar)
    
    def save(self, *args, **kwargs):
        """ Ensure email is copied from User model, if needed """
        # You don't need to store the email in the profile, as it exists in the User model.
        # Just make sure the User email is up-to-date when saving the profile.
        if self.user.email != self.user.email:
            self.user.email = self.user.email
        super().save(*args, **kwargs)
# for multiple images for single products
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.name}"

# custom slider images with product references
class SliderImage(models.Model):
    image = models.ImageField(upload_to='slider/', blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='slider_images', blank=True, null=True)

    def __str__(self):
        return self.title if self.title else "Slider Image"
        


