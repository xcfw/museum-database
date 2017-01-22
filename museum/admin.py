from django.contrib import admin

from .models import Collection

class CollectionAdmin(admin.ModelAdmin):
	fields = ['category', 'type', 'location', 'era',]
	list_display = ('reference', 'category', 'type', 'location', 'era',)
	

admin.site.register(Collection, CollectionAdmin)
