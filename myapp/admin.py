from django.contrib import admin

from .models import DriverProfile, Order, Product, Profile, Review

admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(DriverProfile)
admin.site.register(Order)
admin.site.register(Review)
