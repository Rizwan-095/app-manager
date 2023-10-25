from django.contrib import admin
from .models import App, Subscription, Plan


class PlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'created_at')
    list_display_links = ('id', 'name', 'price')


class AppAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'created_at')
    list_display_links = ('id', 'name', 'owner')


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'app', 'plan', 'isActive', 'created_at')
    list_display_links = ('id', 'app', 'plan')


admin.site.register(Plan, PlanAdmin)
admin.site.register(App, AppAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
