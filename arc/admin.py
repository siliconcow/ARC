from django.contrib import admin
from arc.models import *

class AceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Ace,AceAdmin)
