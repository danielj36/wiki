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
    query = request.GET["q"]
    all_entries = util.list_entries()
    partial_matches = []
    for x in all_entries:
        if query == x:
            return redirect("wiki/"+query)
        elif query in x:
            partial_matches.append(x)
        else:
            continue
    return render(request, "encyclopedia/results.html", {
        "results": partial_matches
        })
