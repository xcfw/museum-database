from django.db import models
from django.utils.safestring import mark_safe
from django.conf import settings
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
		('Art', 'Art'),
		('Book', 'Book'),
		('Diary', 'Diary'),
		('Display', 'Display'),
		('Equipment', 'Equipment'),
		('Flag', 'Flag'),
		('Weapon', 'Weapon'),
		('Medal', 'Medal'),
		('Modern', 'Model'),
		('Insignia', 'Insignia'),
		('Plaque', 'Plaque'),
		('Uniform', 'Uniform'),	
	)
		
	type = models.CharField(max_length=20, choices=TYPE_CHOICE)
	
	location = models.CharField(max_length=50, default=' ')
	
	ERA_CHOICES = (
		('Colonial', 'Colonial'),
		('Boer War', 'Boer War'),
		('WW1', 'World War 1'),
		('WW2', 'World War 2'),
		('Korean War', 'Korean War'),
		('Vietnam War', 'Vietnam War'),
		('Post 1975', 'Post 1975'),
	)
	
	era = models.CharField(max_length=15, choices=ERA_CHOICES, default=' ')
	
	reference = models.CharField(max_length=10, default=' ')
	
	image = models.ImageField(upload_to = settings.UPLOAD_DIR + 'museum/static/museum/database/', default = 'museum/static/museum/database/photo_not_available.png', blank=True)

	def url(self):
		return os.path.join('/','static/museum/database/', os.path.basename(str(self.image)))
	
	def image_tag(self):
		return mark_safe('<img src="{}" width="150" height="150" />'.format(self.url()) ) 	
	
	
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
	image = models.ImageField(upload_to = settings.UPLOAD_DIR + 'museum/static/museum/database/', default = 'museum/static/museum/database/photo_not_available.png')

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
				('Painting', 'Painting'),
				('Drawing', 'Drawing'),
				('Sculpture', 'Sculpture'),
				('Poster', 'Poster'),
				('Photograph', 'Photograph'),
			)
		),
		('Book', (
				('Book', 'Book'),
				('Magazine', 'Magazine'),
				('Journal', 'Journal'),
				('Reference', 'Reference'),
				('Comic', 'Comic'),
			)
		),
		('Diary', 'Diary'),
		('Display', 'Display'),
		('Equipment', (
				('Helmet', 'Helemet'),
				('Binoculars', 'Binoculars'),
				('Canteen', 'Canteen'),
				('Bag', 'Bag'),
				('Pack', 'Pack'),
				('Webbing', 'Webbing'),
			)
		),
		('Weapon', (
				('Axe', 'Axe'),
				('Grenade', 'Grenade'),
				('Cannon', 'Cannon'),
				('Knife', 'Knife'),
				('Rifle', 'Rifle'),
				('Pistol', 'Pistol'),
				('Sword', 'Sword'),
				('Dagger', 'Dagger'),
			)
		),
		('Flag', 'Flag'),
		('Medal', 'Medal'),
		('Model', (
				('Airplane', 'Airplane'),
				('Helicopter', 'Helicopter'),
				('Ship', 'Ship'),
				('Submarine', 'Submarine'),
				('Tank', 'Tank'),
				('APC', 'APC'),
				('Jeep', 'Jeep'),
			)
		),
		('Insignia', 'Insignia'),
		('Plaque', 'Plaque'),
		('Uniform', (
				('Boots', 'Boots'),
				('Socks', 'Socks'),
				('Trousers', 'Trousers'),
				('Skirt', 'Skirt'),
				('Shirt', 'Shirt'),
				('Jacket', 'Jacket'),
				('Tunic', 'Tunic'),
				('Hat', 'Hat'),
				('Belt', 'Belt'),
				('Button', 'Button'),
			)
		),		
	)
	
	type = models.CharField(max_length=20, choices=TYPE_CHOICE)
	
	CONDITION_CHOICES = (
		('New', 'New'),
		('Excellent', 'Excellent'),
		('Very Good', 'Very Good'),
		('Average', 'Average'),
		('Below Average', 'Below Average'),
		('Poor', 'Poor'),
	)
	
	condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
	
	value = models.CharField(max_length=20)
	
	image = models.ImageField(upload_to = settings.UPLOAD_DIR + 'museum/static/museum/database/', default = 'museum/static/museum/database/photo_not_available.png', blank=True)

	def url(self):
		return os.path.join('/','static/museum/database/', os.path.basename(str(self.image)))
	
	def image_tag(self):
		return mark_safe('<img src="{}" width="150" height="150" />'.format(self.url()) ) 
	
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
	image = models.ImageField(upload_to = settings.UPLOAD_DIR + 'museum/static/museum/database/', default = 'museum/static/museum/database/photo_not_available.png')

	def url(self):
		return os.path.join('/','static/museum/database/', os.path.basename(str(self.image)))
	
	def image_tag(self):
		return mark_safe('<img src="{}" width="150" height="150" />'.format(self.url()) ) 	