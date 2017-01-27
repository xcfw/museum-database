from django.shortcuts import render, get_object_or_404
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
	collections = Collection.objects.all().count()
	items = Item.objects.all().count()
	images = CollectionImage.objects.all().count() + ItemImage.objects.all().count()
	
	return render(request, 'museum/index.html', {'collections': collections, 'items': items, 'images': images })
	
#display all Collections
def collections(request):
	collections_list = Collection.objects.all()
	page = request.GET.get('page', 1)
	paginator = Paginator(collections_list, 20)
	try:
		collections = paginator.page(page)
	except PageNotAnInteger:
		collections = paginator.page(1)
	except EmptyPage:
		collections = paginator.page(paginator.num_pages)
	
	return render(request, 'museum/collections.html', { 'collections': collections })
	
#display all items	
def items(request):
	items_list = Item.objects.all()
	page = request.GET.get('page', 1)
	paginator = Paginator(items_list, 20)
	try:
		items = paginator.page(page)
	except PageNotAnInteger:
		items = paginator.page(1)
	except EmptyPage:
		items = paginator.page(paginator.num_pages)
	
	return render(request, 'museum/items.html', { 'items': items })

#display single Collection page
def collectionView(request, ref):
	collection = get_object_or_404(Collection, reference=ref)
	images = CollectionImage.objects.filter(item_id=collection.id)
	items = Item.objects.filter(collection_id=collection.id)
	return render(request, 'museum/collection.html', {'collection': collection, 'images': images, 'items': items })
	
#display single Item Page
def itemView(request, ref):
	item = get_object_or_404(Item, reference=ref)
	images = ItemImage.objects.filter(item_id=item.id)
	collection = get_object_or_404(Collection, id=item.collection_id.id)
	return render(request, 'museum/item.html', {'item': item, 'images': images, 'collection': collection })