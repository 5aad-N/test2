from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Item, Bid, Question

admin.site.register(User, UserAdmin)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'current_price', 'end_date', 'is_active']
    list_filter = ['is_active', 'end_date']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ['item', 'bidder', 'amount', 'created_at']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['item', 'asker', 'question_text', 'asked_at', 'answered_at']
    list_filter = ['asked_at', 'answered_at']
    date_hierarchy = 'asked_at'
