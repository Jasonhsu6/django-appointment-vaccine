from django.contrib import admin
from .models import Appointment


# Register your models here.

# @admin.site.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'first_name', 'last_name', 'birthday', 'email', 'phone')
    list_filter = ('date',)
    search_fields = ("first_name__startswith",)


admin.site.register(Appointment, AppointmentAdmin)


# class WaitListAdmin(admin.ModelAdmin):
#     list_display = ('picked', 'first_name', 'last_name', 'birthday', 'email', 'phone')
#     list_filter = ('picked',)
#
#     def pick(modeladmin, request, queryset):
#         queryset.update(picked=True)
#     pick.short_description = "Mark as picked"
#     actions = [pick]


# admin.site.register(WaitList, WaitListAdmin)
