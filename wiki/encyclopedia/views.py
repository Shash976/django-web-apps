from django.shortcuts import render
from . import util
from .forms import *
import re
import markdown2
import random
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def markdown_to_html(markdown_content):
    html_content = markdown2.markdown(markdown_content)
    return html_content

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    markdown_content=util.get_entry(title)
    if markdown_content == None:
        return render(request, "encyclopedia/error.html")
    html_content = markdown_to_html(markdown_content)
    return render(request, "encyclopedia/entry.html", {"content":html_content, "title": title})
    

def search(request):
    total_entries=util.list_entries() 
    query = request.GET.get('q') #search_query
    results=[] #search_results
    for entry in total_entries:
        if re.search(query, entry, re.IGNORECASE):
            results.append(entry)
            rg=f"^{query}$"
            raw= r'{}'.format(rg)
            if re.search(raw, entry, re.IGNORECASE):
                content=util.get_entry(entry)
                return render(request, "encyclopedia/entry.html", {"content":content, "title": entry.upper()})
    return render(request, "encyclopedia/search.html", {"results":results, "query":query, "res":len(results)!=0})

def new_page(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            markdown_content = form.cleaned_data["content"]
            if title not in util.list_entries():
                util.save_entry(title, markdown_content)
                return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={'title':title}))
    return render(request, "encyclopedia/create.html", {
        "form": NewEntryForm()
        })

def edit_page(request, title):
    markdown_content=util.get_entry(title)
    if request.method == "POST":
        new_content = request.POST.get("content")
        util.save_entry(title, new_content)
        return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={'title': title}))
    return render(request, "encyclopedia/edit.html", {"title":title, "content":markdown_content})

def random_page(request):
    total_entries=util.list_entries()
    total=len(total_entries)
    lucky_num = random.randrange(total)
    title = total_entries[lucky_num]
    return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={'title': title}))