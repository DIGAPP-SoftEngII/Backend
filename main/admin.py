from django.contrib import admin
from .models import Business, Consult, User, Report, Favorite, OccupationStatus, City

# Register your models here.

admin.site.register(User)
admin.site.register(Business)
admin.site.register(Consult)
admin.site.register(Report)
admin.site.register(Favorite)
admin.site.register(OccupationStatus)
admin.site.register(City)