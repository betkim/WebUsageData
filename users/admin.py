from django.contrib import admin
from .models import User
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['phone','address','created_at','updated_at']


# class User(AbstractUser):
#     phone = models.CharField(max_length=15, blank=True)
#     address = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)