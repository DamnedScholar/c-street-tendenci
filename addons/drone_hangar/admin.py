from django.contrib import admin

from .models import AirBnBData


class AirBnBSpiderAdmin(admin.ModelAdmin):
    # Show a list of scraped locations.
    actions = ['summon_airbnb_spider']
    list_filter = ['guests', 'superhost']
    ordering = ['avg_rating']

admin.site.register(AirBnBData, AirBnBSpiderAdmin)
