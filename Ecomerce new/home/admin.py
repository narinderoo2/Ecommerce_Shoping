import admin_thumbnails
from django.contrib import admin
from home.models import Like_User, Product,Comment,Color,Size,Image,Comment,Variants,Category,Contact


# in product list show image inline
@admin_thumbnails.thumbnail('image')
class ProductImageInline(admin.TabularInline):
    model = Image
    extra = 1
    readonly_fields = ('id',)

# all varients in List(have a COLOR,SIZE and PRODUCT)
class ProductVariantsInline(admin.TabularInline):
    model = Variants
    extra = 1
    readonly_fields = ('image',)

@admin_thumbnails.thumbnail('image')
class ImageAdmin(admin.ModelAdmin):
    list_display=['product', 'image','image_thumbnail']

# add all inline as a product
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','price','image_tag','star_average','count_review']
    list_filter = ['title']
    readonly_fields = ('image_tag',)
    inlines = [ProductImageInline,ProductVariantsInline]
    prepopulated_fields = {'slug':('title',)}

class CommentAdmin(admin.ModelAdmin):
    list_display=['comment','id','man_like','product','user']
    search_fields = ['user']

class Like_UserAdmin(admin.ModelAdmin):
    list_display=['user1','id','comment1']
    search_fields = ['user']

class SizeAdmin(admin.ModelAdmin):
    list_display = ['id','name','code']

class ColorAdmin(admin.ModelAdmin):
    list_display=['id','name','code','color_code']

class VariantsAdmin(admin.ModelAdmin):
    list_display=['id','product','size','color','price','quantity','image']

admin.site.register(Product,ProductAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Like_User,Like_UserAdmin)
admin.site.register(Image,ImageAdmin)
admin.site.register(Size,SizeAdmin)
admin.site.register(Color,ColorAdmin)
admin.site.register(Variants,VariantsAdmin)
admin.site.register(Category)
admin.site.register(Contact)
