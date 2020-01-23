from django.shortcuts import render

#3.4 - Creating a view
from django.http import HttpResponse

def index(request):
    #Passed to template engine, matches {{ boldmessage }}
    #Key value pairs employed within the template
    context_dict = {"boldmessage": "Crunchy, creamy, cookie, candy, cupcake!"}

    #Return rendered response to send to client, first parameter is template
    #The render function combines the template data and the context_dict to produce a page
    return render(request, "rango/index.html", context = context_dict)

    #return HttpResponse("Rango says hey there partner! " + "<a href = '/rango/about/'>About</a>")


def about(request):
    context_dict = {"boldmessage": "This tutorial has been put together by Jake Haakanson."}

    return render(request, "rango/about.html", context = context_dict)
    #return HttpResponse("Rango says here is the about page. " + "<a href = '/rango/'>Index</a>")
