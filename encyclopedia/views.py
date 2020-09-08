from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from . import util
import markdown2
from django import forms

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry Title")
    content = forms.CharField(label="Entry Content", widget=forms.Textarea())

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
    query = request.GET["q"].lower()
    all_entries = util.list_entries()
    partial_matches = []
    for x in all_entries:
        if query == x.lower():
            return HttpResponseRedirect("wiki/"+x)
        elif query in x.lower():
            partial_matches.append(x)
        else:
            continue
    return render(request, "encyclopedia/results.html", {
        "results": partial_matches
        })

def newentry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.check_entry(title):
                return render(request, "encyclopedia/creationerror.html", {
                    "title": title
                    })
            util.save_entry(title, content)
            return HttpResponseRedirect("wiki/"+title)
        else:
            return render(request, "encyclopedia/newentry.html", {
                "form": form
                })
    return render(request, "encyclopedia/newentry.html", {
        "form": NewEntryForm()
    })
