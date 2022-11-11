from django.contrib import admin
from .models import Account, User, Shipper, Address
# Register your models here.
admin.register(Account)
admin.register(User)
admin.register(Shipper)
admin.register(Address)