from django.contrib import admin

from .models import Auction, AuctionUserPermission, ImageField, VideoField, AdditionalField, LocationData, Comment


class AuctionUserPermissionInline(admin.TabularInline):
    model = AuctionUserPermission


class ImageFieldInine(admin.TabularInline):
    model = ImageField
    
    
class VideoFieldInine(admin.TabularInline):
    model = VideoField
    
    
class AdditionalFieldInine(admin.TabularInline):
    model = AdditionalField


@admin.register(Auction)
class AuctionModelAdmin(admin.ModelAdmin):
    inlines = (AuctionUserPermissionInline, ImageFieldInine, VideoFieldInine, AdditionalFieldInine,)
    list_display = ('id', 'title', 'starter_price', 'auction_price', 'end_time', 'created', 'updated',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('updated', 'created', 'active',)
    search_fields = ('title', 'description',)
    

admin.site.register(ImageField)
admin.site.register(VideoField)
admin.site.register(AdditionalField)
admin.site.register(LocationData)
admin.site.register(Comment)
