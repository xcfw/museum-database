from django.contrib import admin
import nested_admin

from .models import Collection, Item, CollectionImage, ItemImage


class CollectionImageAdmin(nested_admin.NestedTabularInline):
	model = CollectionImage
	fields = ('image_tag', 'image')
	readonly_fields = ('image_tag',)
	extra = 0
	
class ItemImageAdmin(nested_admin.NestedTabularInline):
	model = ItemImage
	fields = ('image_tag', 'image')
	readonly_fields = ('image_tag',)
	extra = 0

class ItemAdmin(nested_admin.NestedStackedInline):
	model = Item
	fields = ('reference', 'title', 'description', 'condition', 'value', 'type')
	readonly_fields = ('reference',)
	extra = 0
	inlines = [ItemImageAdmin]
	
class CollectionAdmin(nested_admin.NestedModelAdmin):
	fields = ['reference', 'category', 'type', 'location', 'era']
	
	inlines = [CollectionImageAdmin, ItemAdmin]
	
	readonly_fields = ('reference',)
	list_display = ('reference', 'category', 'type', 'location', 'era',)
	

admin.site.register(Collection, CollectionAdmin)
