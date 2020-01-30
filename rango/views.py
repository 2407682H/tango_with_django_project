from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse

from rango.models import Category, Page

from rango.forms import CategoryForm
from rango.forms import PageForm


def about(request):     # View for About page
    context_dict = {"boldmessage": "This tutorial has been put together by Jake Haakanson."}

    return render(request, "rango/about.html", context = context_dict)


def index(request):     # Index from chapter 6
    context_dict = {
        "boldmessage": "Crunchy, creamy, cookie, candy, cupcake!",     # Bold message from earlier
        "categories": Category.objects.order_by("-likes")[:5],         # Add categories list to context_dict
        "pages": Page.objects.order_by("-views")[:5]}                  # Add pages list to context dict

    return render(request, "rango/index.html", context = context_dict)


def show_category(request, category_name_slug):     # Show category view from chapter 6
    context_dict = {}

    try:
        # Get category if it exists and add to context_dict
        category = Category.objects.get(slug = category_name_slug)
        context_dict["category"] = category

        # Get all associated pages, also add to context_dict
        pages = Page.objects.filter(category = category)
        context_dict["pages"] = pages

    except Category.DoesNotExist:
        context_dict["category"] = None
        context_dict["pages"] = None

    return render(request, "rango/category.html", context = context_dict)


def add_category(request):  # Add category view
    form = CategoryForm()

    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit = True)

            return redirect("/rango/")

        else:
            print(form.errors)

    return render(request, "rango/add_category.html", {"form": form})


def add_page(request, category_name_slug):  # Add page view
    try:
        category = Category.objects.get(slug = category_name_slug)

    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect("/rango/")

    form = PageForm()
    if request.method == "POST":
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit = False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse("rango:show_category", kwargs = {"category_name_slug": category_name_slug}))

        else:
            print(form.errors)

    context_dict = {"form": form, "category": category}
    return render(request, "rango/add_page.html", context = context_dict)
