from django.utils.html import format_html
from django.contrib import admin
from .models import Video, Payment

# Register your models here.

class VideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'tutor', 'rate', 'date_created', 'image_display', 'video']

    def image_display(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50"/>'.format(obj.image.url))
        return "No Image"
    
    image_display.allow_tags = True
    image_display.short_description = 'Preview'


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'card_number', 'expiry_date', 'cvv']

admin.site.register(Video, VideoAdmin)
admin.site.register(Payment, PaymentAdmin)
