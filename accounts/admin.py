from django.contrib import admin

from .models import CustomUser, Contact, Address


@admin.register(CustomUser)
class CustomUserModelAdmin(admin.ModelAdmin):
    # inlines = [AuctionUserPermissionInline]
    list_display = ('id', 'username', 'email', 'first_name', 'last_name',)
    # list_filter = ('updated', 'created', 'active',)
    # search_fields = ('title', 'description',)


admin.site.register(Contact)
admin.site.register(Address)
