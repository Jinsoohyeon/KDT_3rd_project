from django.contrib import admin
from .models import Location, TouristReview
# Register your models here.

admin.site.register(Location)
admin.site.register(TouristReview)
# admin.site.register(TripadvisorReview)
# admin.site.register(TripdotComReview)