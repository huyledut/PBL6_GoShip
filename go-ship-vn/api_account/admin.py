from django.contrib import admin
from .models import Account, User, Shipper,Location,Address
# Register your models here.
admin.register(Account)
admin.register(User)
admin.register(Shipper)
admin.register(Location)
admin.register(Address)