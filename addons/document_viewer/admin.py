from django.contrib import admin

from .models import SubscriptionLog


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'timestamp')

admin.site.register(SubscriptionLog, SubscriptionAdmin)
