from django.shortcuts import render, redirect

from . import util
from django import forms

import os
from django.conf import settings

import random
class NewPageForm(forms.Form):
    title = forms.CharField(label="Page title")
    content = forms.CharField(widget=forms.Textarea)

def index(request):
    if request.method == "POST":
        entrySelected = request.POST.get("entrySelected").lower()
        for e in util.list_entries():
            if e.lower() == entrySelected:
                return render(request, "encyclopedia/wiki.html", {
                "entry": entrySelected,
                "entries": util.get_entry(entrySelected),
                "title": entrySelected
                })

        return render(request, "encyclopedia/error.html", {
        "entry": entrySelected,
        "errorMessage": "page not found."
        })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, entry):
    # Make sure the entry is in list
    if util.get_entry(entry) == None:
        return render(request, "encyclopedia/error.html", {
            "entry": entry,
            "errorMessage": "page not found."
        })

    return render(request, "encyclopedia/wiki.html", {
        "entry": entry,
        "entries": util.get_entry(entry),
        "title": entry,
    })


def creatNewPage(request):
    if request.method == "POST":
        newEntry = NewPageForm(request.POST)
        if newEntry.is_valid():
            title = newEntry.cleaned_data["title"].capitalize()
            for t in util.list_entries():
                if title == t.capitalize():    
                    return render(request, "encyclopedia/error.html", {
                        "entry": title,
                        "errorMessage": "entry already exists."
                    })
            content = newEntry.cleaned_data["content"]

            util.save_entry(title, content)

            return redirect("wiki", entry=title)

    return render(request, "encyclopedia/newPage.html", {
        "form": NewPageForm
    })

def random_page(request):
    # Select Random entry
    entries = util.list_entries()
    if not entries:
        return render(request, "encyclopedia/error.html", {
            "entry": "Encyclopedia is empty",
            "errorMessage": "Try add new entry."
        })
    random_entry = random.choice(entries)

    return render(request, "encyclopedia/wiki.html", {
        "entry": random_entry,
        "entries": util.get_entry(random_entry)
    })


def edit_page(request, title):
    if request.method == "POST":
        # Extract data directly from the form
        title = request.POST.get("title")
        content = request.POST.get("content")

        # Save updated entry
        util.save_entry(title, content)
        return redirect("wiki", entry=title)
    
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "content": util.get_entry(title)
    })