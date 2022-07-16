from django.contrib import admin
from .models import TripNews
from .models import NewsSummery, InputKeyword
# Register your models here.

admin.site.register(TripNews)
admin.site.register(NewsSummery)
admin.site.register(InputKeyword)