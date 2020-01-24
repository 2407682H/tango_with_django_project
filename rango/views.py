from django.shortcuts import render
from rango.models import Category, Page

#3.4 - Creating a view
from django.http import HttpResponse

"""def index(request):
    #Passed to template engine, matches {{ boldmessage }}
    #Key value pairs employed within the template
    context_dict = {"boldmessage": "Crunchy, creamy, cookie, candy, cupcake!"}

    #Return rendered response to send to client, first parameter is template
    #The render function combines the template data and the context_dict to produce a page
    return render(request, "rango/index.html", context = context_dict)

    #return HttpResponse("Rango says hey there partner! " + "<a href = '/rango/about/'>About</a>")
"""


def about(request):
    context_dict = {"boldmessage": "This tutorial has been put together by Jake Haakanson."}

    return render(request, "rango/about.html", context = context_dict)
    #return HttpResponse("Rango says here is the about page. " + "<a href = '/rango/'>Index</a>")


#Index from chapter 6
def index(request):
    #Query database for all categories, order by likes descending
    #Obtain top 5 by likes and place this list in context dictionary
    topFiveCategories = Category.objects.order_by("-likes")[:5]

    context_dict = {}

    #Bold message from earlier, add categories list to context_dict
    context_dict["boldmessage"] = "Crunchy, creamy, cookie, candy, cupcake!"
    context_dict["categories"] = topFiveCategories

    #Add pages list to context dict
    context_dict["pages"] = Page.objects.order_by("-views")[:5]

    return render(request, "rango/index.html", context = context_dict)

#Show category view from chapter 6
def show_category(request, category_name_slug):
    context_dict = {}

    try:
        #Get category if it exists and add to context_dict
        category = Category.objects.get(slug = category_name_slug)
        context_dict["category"] = category

        #Get all associated pages, also add to context_dict
        pages = Page.objects.filter(category = category)
        context_dict["pages"] = pages

    except Category.DoesNotExist:
        context_dict["category"] = None
        context_dict["pages"] = None

    return render(request, "rango/category.html", context = context_dict)
