from django.contrib import admin
from .models import Excursion, Poll

@admin.register(Excursion)
class ExcursionAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "guide", "n_visitors", "phone", "poll")
    list_filter = ("guide", "poll")
    search_fields = ("guide", "phone")
    ordering = ("-date",)
    date_hierarchy = "date"

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ("id", "week_start", "week_end", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("week_start", "week_end")

#@admin.register(User)
#class UserAdmin(admin.ModelAdmin):
#    list_display = ("fullname", "tg_username", "card_id", "role")
#    search_fields = ("fullname", "tg_username", "card_id")
#   list_filter = ("role",)