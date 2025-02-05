from django.contrib import admin
from Base_App.models import *

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'user_name', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('user_name',)

# Register models
admin.site.register(ItemList)
admin.site.register(Items)
admin.site.register(AboutUs)
admin.site.register(Feedback)
admin.site.register(BookTable)
admin.site.register(Order, OrderAdmin)  # Register Order with custom OrderAdmin class
