from django.shortcuts import render
from .models import Link
from django.core.paginator import Paginator

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