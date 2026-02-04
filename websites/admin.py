from django.contrib import admin

from websites.models import FeaturesModel, Order, OrderItem,  SliderModel,productsmodel,AboutSectionhomeModel,TestimonialsModel,Product
from websites.models import ProductsHeroModel

# Register your models here.
class SliderModelAdmin(admin.ModelAdmin):
    list_display = ['slider_title', 'slider_description', 'slider_image', 'slider_btn_title',]
admin.site.register(SliderModel, SliderModelAdmin)

class FeaturesModelAdmin(admin.ModelAdmin):
    list_display = ['section_title', 'feature_icon', 'feature_title', 'feature_description']
    search_fields = ['feature_title', 'feature_description']
    list_filter = ['section_title']

admin.site.register(FeaturesModel, FeaturesModelAdmin)

class productsmodelAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'product_weight', 'product_price', 'product_image']
    search_fields = ['product_name']
admin.site.register(productsmodel, productsmodelAdmin)

class AboutSectionhomeModelAdmin(admin.ModelAdmin):
    list_display = ['about_title', 'about_description', 'about_image', 'about_btn_title',]
    search_fields = ['about_title', 'about_description']
admin.site.register(AboutSectionhomeModel, AboutSectionhomeModelAdmin)
    
class TestimonialsModelAdmin(admin.ModelAdmin):
    list_display = ['Testimonials_star', 'Testimonials_description', 'Testimonials_name_address']
admin.site.register(TestimonialsModel, TestimonialsModelAdmin)

class ProductsHeroModelAdmin(admin.ModelAdmin):
    list_display = ('hero_title', 'hero_description', 'hero_image')
    search_fields = ('hero_title', 'hero_description')

admin.site.register(ProductsHeroModel, ProductsHeroModelAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'weight', 'created_at')
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Product, ProductAdmin)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0




class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "total_amount", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("name", "phone")

admin.site.register(Order, OrderAdmin)
   