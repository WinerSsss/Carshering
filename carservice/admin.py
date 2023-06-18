from django.contrib import admin
from carservice import models

admin.site.register(models.Car)
admin.site.register(models.Offer)
admin.site.register(models.User)
admin.site.register(models.Rent)
