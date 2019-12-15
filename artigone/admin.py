# Register your models here.
from django.contrib import admin
from .models import *

admin.site.register(Game)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(PrimaryImage)
admin.site.register(SecondaryImage)
