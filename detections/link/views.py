from django.shortcuts import render,redirect,get_object_or_404
from .models import Link,word
from django.core.paginator import Paginator
from django.contrib import messages
from .general import *
import os

# Create your views here.


def index(request):
    links = Link.objects.all()
    words = list()

    for word in list(links):
        if word is not None:
            words += word.get_words()
    
    kw = set(words)
    final_kw = list(kw)

    try:
        query = request.GET["search"]
        
        if query:
            links = links.filter(keywords__contains = query)

    finally:
        paginator = Paginator(links,10 ) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,'index.html',{'page_obj':page_obj, 'final_kw': final_kw})

def badwords(request):
    try:
        add = request.GET["add"]
        if len(word.objects.filter(name=add.strip())) == 0:
            print("Doesnt Exist")
            it = word(name=add.strip())
            it.save()
            messages.info(request, "The word is added")
        else:
            messages.info(request, "The word exists")
    except:
        print()

    finally:
        words = word.objects.all()
        try:
            query = request.GET["searchb"]
            if query:
                words = words.filter(name = query.strip())
        except:
            print()    
        paginator = Paginator(words,20) 
        page_number = request.GET.get('page')
        word_obj = paginator.get_page(page_number)
        return render(request,'badwords.html',{'word_obj':word_obj})

def remove(request,id):
    item = get_object_or_404(word, id=id)
    bad_item = word.objects.filter(id=item.id)[0]
    bad_item.delete()
    messages.info(request, "The word is removed")
    return redirect('badwords')


def run(request):
    module_dir = os.path.dirname(__file__)  
    file_path = os.path.join(module_dir, '../static/attack_links.txt') 

    Link.objects.all().delete()
    words = word.objects.all()
    bad_words = []
    for w in words:
        bad_words.append(w.name)
    techniques = list(file_to_setl(file_path))

    for link1 in techniques:
        print("working on",link1)
        id1 = link1[-5:]
        detcn,soup = detection(link1)
        mitigation = mitigations(soup)
        if detcn is not None:
            k = keywords(detcn,bad_words)
            new = Link()
            new.name=str(id1)
            new.link=str(link1)
            new.detection=str(detcn)
            new.keywords=list_to_str(k)
            new.mitigate=list_to_str(mitigation)
            new.save()
    return redirect('/')