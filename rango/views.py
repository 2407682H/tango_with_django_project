from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from rango.models import Category, Page

from rango.forms import CategoryForm, PageForm
from rango.forms import UserForm, UserProfileForm


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


@login_required
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


@login_required
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


def register(request):
    # Lets the template know if registration was successful
    registered = False

    if request.method == "POST":
        # Grab info from the raw form info
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # Check that the two forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # Store user form data in the database
            user = user_form.save()

            # Hash password with set_password function
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit = False)
            profile.user = user

            # Check if user provided a profile picture
            if "picture" in request.FILES:
                profile.picture = request.FILES["picture"]

            # Save the UserProfile model instance
            profile.save()

            # Indicate that registration was successful
            registered = True

        else:
            # Invalid forms, print problems
            print(user_form.errors, profile_form.errors)

    else:
        # Not a HTTP POST so display some blank forms ready for input
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, "rango/register.html", context = {"user_form": user_form, "profile_form": profile_form, "registered": registered})


def user_login(request):
    if request.method == "POST":
        # Retrieve username and password
        # Use req.POST.get as it will return None instead of throwing an error
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check all is well
        user = authenticate(username = username, password = password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse("rango:index"))

            else:
                return HttpResponse("Your Rango account is disabled.")

        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, "rango/login.html")


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse("rango:index"))


@login_required
def restricted(request):
    # return HttpResponse("Since you're logged in, you can see this text!")
    return render(request, "rango/restricted.html")
