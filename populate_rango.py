import os
import random

os.environ.setdefault(  "DJANGO_SETTINGS_MODULE",
			"tango_with_django_project.settings")


import django

django.setup()

from rango.models import Category, Page


def pop():
    python_pages = [
			{"title" : "Official python tutorial",
			 "url" : "http://docs.python.org/3/tutorial/"},
			{"title" : "How to think like a compsci",
			 "url" : "http://www.greenteapress.com/thinkpython/"},
			{"title" : "Learn python in 10 Minutes",
			 "url" : "http://www.korokithakis.net/tutorials/python/"},
    ]

    django_pages = [
			{'title':'Official Django Tutorial',
			 'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/'},
			{'title':'Django Rocks',
			 'url':'http://www.djangorocks.com/'},
			{'title':'How to Tango with Django',
			 'url':'http://www.tangowithdjango.com/'}
    ]

    other_pages = [
			{'title':'Bottle',
			 'url':'http://bottlepy.org/docs/dev/'},
			{'title':'Flask',
			 'url':'http://flask.pocoo.org'}
    ]

    cats = {
		'Python': {'pages': python_pages},
		'Django': {'pages': django_pages},
		'Other Frameworks': {'pages': other_pages}
    }


    initial = 128 #Used to populate views and likes

    for cat, cat_data in cats.items():
        c = add_cat(cat, initial)
        initial = (initial / 2) #Divide initial by 2 every time for exercise
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], views = random.randint(0, 150))


    for c in Category.objects.all():
        for p in Page.objects.filter(category = c):
            print(f'- {c}: {p}')

def add_page(cat, title, url, views = 0):
    p = Page.objects.get_or_create(category = cat, title = title)[0]
    p.url = url
    p.views = views
    p.save()
    return p

def add_cat(name, viewsAndLikesValue):
    c = Category.objects.get_or_create(name = name, views = viewsAndLikesValue, likes = (viewsAndLikesValue / 2))[0]
    c.save()
    return c

if __name__ == "__main__":
    print("Starting Rango population script...")
    pop()
