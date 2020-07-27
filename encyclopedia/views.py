from django.shortcuts import render
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
