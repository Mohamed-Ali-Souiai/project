from django.contrib import admin
from review.models import Ticket, Review


# Register your models here.
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'user')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticket', 'headline', 'body', 'user')


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)