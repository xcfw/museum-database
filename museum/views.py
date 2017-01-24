from django.shortcuts import render, get_object_or_404
from .models import *

def index(request):
	collections = Collection.objects.all().count()
	items = Item.objects.all().count()
	images = CollectionImage.objects.all().count() + ItemImage.objects.all().count()
	
	return render(request, 'museum/index.html', {'collections': collections, 'items': items, 'images': images })
	
#display all Collections
def collections(request):
	collections = Collection.objects.all()
	
	return render(request, 'museum/collections.html', { 'collections': collections })
	
#display all items	
def items(request):
	items = Item.objects.all()
	
	return render(request, 'museum/items.html', { 'items': items })

#display single Collection page
def collectionView(request, ref):
	collection = get_object_or_404(Collection, reference=ref)
	images = CollectionImage.objects.filter(item_id=collection.id)
	items = Item.objects.filter(collection_id=collection.id)
	return render(request, 'museum/collection.html', {'collection': collection, 'images': images, 'items': items })