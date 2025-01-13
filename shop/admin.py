from django.contrib import admin
from .models import Product, Cart, CartItem, Order, Profile
from .models import SliderImage
from .models import Product, ProductImage







# Custom admin class for the Product model
class ProductAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('name', 'price', 'description', 'image', 'created_at')

    # Fields that will be clickable for sorting
    list_display_links = ('name',)

    # Enable search functionality for specific fields
    search_fields = ('name', 'description')

    # Add filters to narrow down results
    list_filter = ('price', 'created_at')

    # Add a feature to paginate the products
    list_per_page = 20

    # Allow editing certain fields directly in the list view
    list_editable = ('price',)

# Register the Product model with the custom admin interface
admin.site.register(Product, ProductAdmin)


# Custom admin class for the Cart model
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1  # Show 1 extra empty form to add a new item
    fields = ('product', 'quantity')  # Fields to display for CartItem

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)
    inlines = [CartItemInline]  # Add CartItemInline to the Cart admin

# Register the Cart model with the custom admin interface
admin.site.register(Cart, CartAdmin)


# Custom admin class for the CartItem model
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'get_subtotal')
    search_fields = ('cart__user__username', 'product__name')

    def get_subtotal(self, obj):
        return obj.get_subtotal()

    get_subtotal.short_description = 'Subtotal'  # Custom label for the subtotal field

# Register the CartItem model with the custom admin interface
admin.site.register(CartItem, CartItemAdmin)


# Custom admin class for the Order model
def mark_as_shipped(modeladmin, request, queryset):
    queryset.update(shipped=True)
mark_as_shipped.short_description = "Mark selected orders as shipped"

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'cart', 'created_at', 'shipped', 'get_total_price')  # Added total price
    list_filter = ('shipped', 'created_at')
    search_fields = ('user__username', 'cart__id')
    actions = [mark_as_shipped]  # Add the action to mark orders as shipped
    readonly_fields = ('get_total_price',)  # Make get_total_price readonly in the admin view

    def get_total_price(self, obj):
        return obj.get_total_price()

    get_total_price.short_description = 'Total Price'  # Custom label for the field

# Register the Order model with the custom admin interface
admin.site.register(Order, OrderAdmin)


# Register the Profile model with the default admin interface
admin.site.register(Profile)

# Custom admin class for the SliderImage model
class SliderImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'image')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)

admin.site.register(SliderImage, SliderImageAdmin)

# Inline model to handle product images
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Display one extra empty form for adding a new image

# Register models to the admin site
admin.site.register(ProductImage)


