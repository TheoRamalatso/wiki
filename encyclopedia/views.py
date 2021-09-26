from markdown2 import markdown
from . import util
from random import randint
from django.shortcuts import render,redirect


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
#gets an entry 
def entry(request, title):
    # get an entry by tittle
    content = util.get_entry(title.strip())
    #unable to fetch:
    if content == None:
        content = "The Page entered does not exist !"
        #true, convert Markdown syntax into HTML.
    content = markdown(content)
    return render(request, "encyclopedia/entry.html", {'content': content, 'title': title})


#ReverseMatch
def edit(request, title):
    content = util.get_entry(title.strip())
    if content == None:
        return render(request, "encyclopedia/edit.html", {'error': " Error 404"})
    # If the form has been submitted
    if request.method == "POST":
        
        content = request.POST.get("content").strip()
        #there hasn't been any submission of a content
        if content == "":
            return render(request, "encyclopedia/edit.html", {"message": "Unable to save with empty field.", "title": title, "content": content})
        # positive
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/edit.html", {'content': content, 'title': title})

def search(request):
    # get query and strip it
    q = request.GET.get('q').strip()
    # if query exits in entries
    if q in util.list_entries():
        return redirect("entry", title=q)
    return render(request, "encyclopedia/search.html", {"entries": util.search(q), "q": q})

def create(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()
        if title == "" or content == "":
            return render(request, "encyclopedia/add.html", {"message": "Unable to save an empty field.", "title": title, "content": content})
        if title in util.list_entries():
            return render(request, "encyclopedia/add.html", {"message": "Title exists. type in a different one.", "title": title, "content": content})
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/add.html")
#randomize pages
def random_page(request):
    entries = util.list_entries()
    random_title = entries[randint(0, len(entries)-1)]
    return redirect("entry", title=random_title)