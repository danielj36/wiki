from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    soup = util.get_entry(name)
    if soup == None:
        return render(request, "encyclopedia/error.html", {
            "name": name
            })
    else:
        return render(request, "encyclopedia/entry.html", {
            "name": name, "content": markdown2.markdown(soup)
            })

def search(request):
    match = False
    query = request.GET["q"]
    all_entries = util.list_entries()
    partial_matches = []
    for x in all_entries:
        if query == x:
            match = True
        elif query in x:
            partial_matches += x
        else:
            continue
    if match:
        return redirect("wiki/"+query)
    elif partial_matches == []:
        return render(request, "encyclopedia/noresults.html")
    else:
        return render(request, "encyclopedia/results.html", {
            "results": partial_matches
            })
