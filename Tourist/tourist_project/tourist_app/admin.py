from django.contrib import admin
from tourist_app.models import places

# Register your models here.
class placesAdmin(admin.ModelAdmin):
    list_display=['id','pname','days','person','price','description']

admin.site.register(places , placesAdmin)