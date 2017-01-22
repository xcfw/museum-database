from django.db import models

class Collection(models.Model):
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
	
	def get_reference(self):
		obj = Collection.objects.filter(category=self.category).count()
		print(obj)
		
		if obj == 1:
			return self.category + '0001'
			
		else:
			
			ref = self.category
			obj = Collection.objects.filter(category=self.category).order_by('-id')[0]
			print(obj.reference)
			incr_num = int(obj.id) + 1
			num = '000' + str(incr_num)
		
		while len(num) > 4:
			num = num[1:]
			
		return ref + num
		
	def save(self, *args, **kwargs):
		if not self.pk:
			obj = Collection.objects.filter(category=self.category).count()
		
			if obj < 1:
				self.reference = self.category + '0001'
			
			else:
			
				ref = self.category
				obj = Collection.objects.filter(category=self.category).order_by('-id')[0]
				print(obj.reference)
				incr_num = obj.reference[-4:].strip()
				print(incr_num)
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
		
	

	