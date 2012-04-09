from django.contrib import admin
from arc.models import *

class AceAdmin(admin.ModelAdmin):
    pass

class CommandTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Ace,AceAdmin)
admin.site.register(CommandType,CommandTypeAdmin)
