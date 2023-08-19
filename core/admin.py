from django.contrib import admin
from core.models import User, Address, Contact

# Register your models here.
admin.site.register(Address)
admin.site.register(Contact)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')
admin.site.register(User, UserAdmin)
