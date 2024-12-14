from lists.models import Item, List
from django.shortcuts import redirect, render


def home_page(request):
    return render(request, 'lists/home.html',)

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST.get("item_text", ''), list=list_)
    return redirect(f'/lists/{list_.id}/')    
    

def view_list(request, id):
    list_ = List.objects.get(id=id)
    items = Item.objects.filter(list=list_)
    return render(request, 'lists/list.html', {"list": list_})

def add_item(request, id):
    list_ = List.objects.get(id=id)
    Item.objects.create(text=request.POST.get("item_text", ''), list=list_)
    return redirect(f'/lists/{list_.id}/')
