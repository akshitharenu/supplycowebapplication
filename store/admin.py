from django.contrib import admin
from .models import Customerdetails, Category, Product, Cart, contact, Feedback, staff, stock, DailyReport, Order,Orderdetail,Adds,ProductReview


# Register your models here.
class CustomerdetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'locality', 'city', 'mobno', 'rationcardno', 'rationcardphoto')
    list_filter = ('city', 'mobno')
    list_per_page = 10
    search_fields = ('locality', 'city', 'mobno')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category_image', 'is_active', 'is_featured', 'updated_at', 'choice')
    list_editable = ('slug', 'is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured', 'choice')
    list_per_page = 10
    search_fields = ('title', 'description')
    prepopulated_fields = {"slug": ("title",)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'product_image', 'is_active', 'is_featured', 'updated_at')
    list_editable = ('slug', 'category', 'is_active', 'is_featured')
    list_filter = ('category', 'is_active', 'is_featured')
    list_per_page = 10
    search_fields = ('title', 'category', 'short_description')
    prepopulated_fields = {"slug": ("title",)}


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at')
    list_editable = ('quantity',)
    list_filter = ('created_at',)
    list_per_page = 20
    search_fields = ('user', 'product')


class staffAdmin(admin.ModelAdmin):
    list_display = ('name', 'staff_id', 'password')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'ordered_date')
    list_editable = ['status']
    list_filter = ('status', 'ordered_date')
    list_per_page = 20
    search_fields = ('user', 'product')


class StockAdmin(admin.ModelAdmin):
    list_display = ('product','stock', 'date')
    list_editable = ['stock']
    readonly_fields = (['image_tag'])

    # def image_tag(self, obj):
    #     return obj.image_tag


admin.site.register(Customerdetails, CustomerdetailsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(staff)
admin.site.register(stock, StockAdmin)
admin.site.register(DailyReport)
admin.site.register(contact)
admin.site.register(Orderdetail)
admin.site.register(Feedback)
admin.site.register(Adds)
admin.site.register(ProductReview)