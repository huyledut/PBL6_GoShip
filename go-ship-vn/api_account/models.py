from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import time


class Account(models.Model):
    list_roles = (
            (1, 'User'),
            (2, 'Shipper'),
            (3, 'Admin')
        )
    phone_number = models.CharField(max_length=11, null =False, primary_key=True)
    password = models.CharField(max_length=255, null=False)
    role = models.IntegerField(default=0, choices=list_roles)
    token_device = models.CharField(max_length=255, null= True, blank=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(db_index=True, auto_now=True)

    class Meta:
        db_table = 'Account'
        ordering = ['created_at']
    def __str__(self):
        return self.phone_number


class Location(models.Model):
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)


class Address(models.Model):
    address_notes = models.CharField(max_length= 255)
    location = models.ForeignKey(Location, related_name='Location', null=True, on_delete=models.CASCADE)


class User(models.Model):
    user_id = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100, default = 'User')
    list_gender=(
        (0,'None'),
        (1,'Male'),
        (2,'Female')
    )
    gender = models.IntegerField(default=0, choices=list_gender)
    address = models.OneToOneField(Address, related_name='Address', on_delete=models.CASCADE, null =True)
    avatar_url = models.CharField(null= True, max_length=255, blank=True)
    distance_view= models.IntegerField(default=10)

class Shipper(models.Model):
    user_id = models.OneToOneField(
        Account, 
        on_delete=models.CASCADE, 
        primary_key=True)
    name = models.CharField(max_length=100, default = 'User')
    list_gender=(
        (0,'None'),
        (1,'Male'),
        (2,'Female')
    )
    gender = models.IntegerField(default=0, choices=list_gender)
    address = models.OneToOneField(
        Address, 
        on_delete=models.CASCADE,
        null =True)
    location = models.OneToOneField(Location, on_delete=models.CASCADE,null =True) 
    list_confirmed =(
        (0,'UnConfirm'),
        (1,'Confirming'),
        (2,'Confirmed'),
        (-1,'Deny')
    ) 
    url_identification_top = models.CharField(max_length=255,null=True)
    url_identification_back = models.CharField(max_length=255,null =True)
    identification_info = models.CharField(max_length=500, null=True, blank =True)
    url_face_video = models.CharField(max_length=255,null = True)
    confirmed = models.IntegerField(default=0, choices=list_confirmed)
    distance_receive= models.IntegerField(default=10)
