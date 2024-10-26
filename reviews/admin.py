from django.contrib import admin
from .models import Reviews

# Register your models here.
class ReviewsAdmin(admin.ModelAdmin):
    list_display =['user', 'product', 'ratings']
admin.site.register(Reviews, ReviewsAdmin)
