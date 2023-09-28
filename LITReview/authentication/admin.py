from django.contrib import admin
from django.conf import settings
from authentication.models import UserFollows, User


# Register your models here.
class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ('user', 'followed_user', 'id')


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'id')


admin.site.register(UserFollows, UserFollowsAdmin)
admin.site.register(User, UserAdmin)
