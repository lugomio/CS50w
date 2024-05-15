from django.shortcuts import render, redirect
import markdown2, random
from random import choice

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def add(request):
    title = request.POST.get("title", "");
    content = request.POST.get("content", "");

    if util.get_entry(title) != None:
        return render(request, "encyclopedia/add.html", {
            "error": True,
            "content": content
        })


    if content != "" and title != "":
        util.save_entry(title, content)

    return render(request, "encyclopedia/add.html")


def edit(request):
    title = request.POST.get('title', '')
    newContent = request.POST.get('content', '')

    if newContent != '':
        util.save_entry(title, newContent)
        return redirect(f"/{title}")
    else:
        content = util.get_entry(title)

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })


def search(request):
    param = request.GET.get('q', '')
    matchEntry = util.get_entry(param)

    if matchEntry == None:
        allSimilarEntries = list(filter(lambda entry: param.lower() in entry.lower(), util.list_entries()))
        return render(request, "encyclopedia/search.html", {
            "search": param,
            "entries": allSimilarEntries
        })
    else:
        return redirect(f"/{param}")


def entry(request, title):
    entry = util.get_entry(title)

    if entry == None:
        return render(request, "encyclopedia/404.html")
    else:
        entry = markdown2.markdown(entry)

        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": entry
        })


def random(request):
    entries = util.list_entries()
    random_entry = choice(entries)
    return redirect(f"/{random_entry}")