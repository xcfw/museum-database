from django.db import models
from django.utils.safestring import mark_safe
import os

class Collection(models.Model):
	
	title = models.CharField(max_length=140, default=' ')
	
	CATEGORY_CHOICE = (
		('NAVY', 'Navy'),
		('ARMY', 'Army'),
		('RAAF', 'RAAF'),
		('CIV', 'Civilan'),
		('GEN', 'General'),
	)
	
	category = models.CharField(max_length=4, choices=CATEGORY_CHOICE)
	
	TYPE_CHOICE = (
		('ART', 'Art'),
		('BOOK', 'Book'),
		('DIARY', 'Diary'),
		('DISPLAY', 'Display'),
		('EQUIPMENT', 'Equipment'),
		('FLAG', 'Flag'),
		('WEAPON', 'Weapon'),
		('MEDAL', 'Medal'),
		('MODEL', 'Model'),
		('INSIGNIA', 'Insignia'),
		('PLAQUE', 'Plaque'),
		('UNIFORM', 'Uniform'),	
	)
		
	type = models.CharField(max_length=20, choices=TYPE_CHOICE)
	
	location = models.CharField(max_length=50, default=' ')
	
	ERA_CHOICES = (
		('COLONIAL', 'Colonial'),
		('BOER', 'Boer War'),
		('WW1', 'World War 1'),
		('WW2', 'World War 2'),
		('KOREA', 'Korean War'),
		('VIETNAM', 'Vietnam War'),
		('MODERN', 'Post 1975'),
	)
	
	era = models.CharField(max_length=15, choices=ERA_CHOICES, default=' ')
	
	reference = models.CharField(max_length=10, default=' ')
	
	def save(self, *args, **kwargs):
		if not self.pk:
			obj = Collection.objects.filter(category=self.category).count()
		
			if obj < 1:
				self.reference = self.category + '0001'
			
			else:
			
				ref = self.category
				obj = Collection.objects.filter(category=self.category).order_by('-id')[0]
				incr_num = obj.reference[-4:].strip()
		
				incr_num = int(incr_num) + 1
				num = '000' + str(incr_num)
		
				while len(num) > 4:
					num = num[1:]
			
				self.reference = ref + num
			
		super(Collection, self).save(*args, **kwargs)
		
		
	
class CollectionImage(models.Model):
	item_id = models.ForeignKey(Collection, on_delete=models.CASCADE)
	image = models.ImageField(upload_to = 'museum/static/museum/database/', default = 'museum/static/museum/database/photo_not_available.png')

	def url(self):
		return os.path.join('/','static/museum/database/', os.path.basename(str(self.image)))
	
	def image_tag(self):
		return mark_safe('<img src="{}" width="150" height="150" />'.format(self.url()) ) 
		
class Item(models.Model):
	collection_id = models.ForeignKey(Collection, on_delete=models.CASCADE)
	reference = models.CharField(max_length=15)
	title = models.CharField(max_length=40)
	description = models.TextField()
	
	TYPE_CHOICE = (
		('Art', (
				('PAINTING', 'Painting'),
				('DRAWING', 'Drawing'),
				('SCULPTURE', 'Sculpture'),
				('POSTER', 'Poster'),
			)
		),
		('Book', (
				('BOOK', 'Book'),
				('MAGAZINE', 'Magazine'),
				('JOURNAL', 'Journal'),
				('REFERENCE', 'Reference'),
				('COMIC', 'Comic'),
			)
		),
		('DIARY', 'Diary'),
		('DISPLAY', 'Display'),
		('Equipment', (
				('HELMET', 'Helemet'),
				('BINOCULARS', 'Binoculars'),
				('CANTEEN', 'Canteen'),
				('BAG', 'Bag'),
				('PACK', 'Pack'),
				('WEBBING', 'Webbing'),
			)
		),
		('Weapon', (
				('AXE', 'Axe'),
				('GRENADE', 'Grenade'),
				('CANNON', 'Cannon'),
				('KNIFE', 'Knife'),
				('RIFLE', 'Rifle'),
				('PISTOL', 'Pistol'),
				('SWORD', 'Sword'),
				('DAGGER', 'Dagger'),
			)
		),
		('FLAG', 'Flag'),
		('MEDAL', 'Medal'),
		('Model', (
				('AIRPLANE', 'Airplane'),
				('HELICOPTER', 'Helicopter'),
				('SHIP', 'Ship'),
				('SUBMARINE', 'Submarine'),
				('TANK', 'Tank'),
				('APC', 'APC'),
				('JEEP', 'Jeep'),
			)
		),
		('INSIGNIA', 'Insignia'),
		('PLAQUE', 'Plaque'),
		('Uniform', (
				('BOOTS', 'Boots'),
				('SOCKS', 'Socks'),
				('TROUSERS', 'Trousers'),
				('SKIRT', 'Skirt'),
				('SHIRT', 'Shirt'),
				('JACKET', 'Jacket'),
				('TUNIC', 'Tunic'),
				('HAT', 'Hat'),
				('BELT', 'Belt'),
				('BUTTON', 'Button'),
			)
		),		
	)
	
	type = models.CharField(max_length=20, choices=TYPE_CHOICE)
	
	CONDITION_CHOICES = (
		('NEW', 'New'),
		('EXCELLENT', 'Excellent'),
		('VERYGOOD', 'Very Good'),
		('AVERAGE', 'Average'),
		('BELOWAVERAGE', 'Below Average'),
		('POOR', 'Poor'),
	)
	
	condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
	
	value = models.CharField(max_length=20)
	
	def save(self, *args, **kwargs):
		if not self.pk:
			obj = Item.objects.filter(collection_id=self.collection_id).count()
			new_obj = Collection.objects.get(id=self.collection_id.id)
			if obj < 1:
				
				self.reference = new_obj.reference + 'A'
			
			else:
			
				ref = new_obj.reference
				obj = Item.objects.filter(collection_id=self.collection_id).order_by('-id')[0]
				print(obj.reference)
				incr = obj.reference[-4:].strip()
				
				incr = ''.join([i for i in incr if not i.isdigit()])
				
				lpart = incr.rstrip('Z')
				if not lpart:
					new_s = 'A' * (len(incr) + 1)
				else:
					num_replacements = len(incr) - len(lpart)
					new_s = lpart[:-1] + (chr(ord(lpart[-1]) + 1) if lpart[-1] != 'Z' else 'A')
					new_s += 'A' * num_replacements
			
				self.reference = ref + new_s
			
		super(Item, self).save(*args, **kwargs)

class ItemImage(models.Model):
	item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
	image = models.ImageField(upload_to = 'museum/static/museum/database/', default = 'museum/static/museum/database/photo_not_available.png')

	def url(self):
		return os.path.join('/','static/museum/database/', os.path.basename(str(self.image)))
	
	def image_tag(self):
		return mark_safe('<img src="{}" width="150" height="150" />'.format(self.url()) ) 	