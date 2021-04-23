from django.contrib import admin
from order.models import ShopCart,OrderInfo,OrderProduct,Payment,Wishlist


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['user','quantity','comment','price', 'amount']
    list_filter = ['user']

class OrderProductline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ['user','product','quantity','price', 'amount']
    can_delete = False
    extra = 0

class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','phone','city', 'total','status','create_at']
    list_filter = ['status']
    readonly_fields = ('user','address','city','country','phone','first_name','ip','last_name','phone','city','total')
    can_delete = False
    inlines = [OrderProductline]

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['card_number', 'user', 'full_name','last_month','cvc', 'email','status']
    list_filter = ['status']
    can_delete = False

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['order_id','product','user','quantity','price', 'amount']
    list_filter = ['user']

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['product','user','variant']
    list_filter = ['user']

admin.site.register(ShopCart,ShopCartAdmin)
admin.site.register(OrderInfo,OrderInfoAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(Wishlist,WishlistAdmin)
