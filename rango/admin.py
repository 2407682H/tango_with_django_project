from django.contrib import admin
from rango.models import Category, Page

class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url")

admin.site.register(Category)
admin.site.register(Page, PageAdmin)

"""
#From django tutorial
from rango.models import Question, Choice

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "pub_date", "was_published_recently")

    fieldsets = [
		(None, 			{"fields": ["question_text"]}),
		("Date Information", 	{"fields": ["pub_date"], "classes": ["collapse"]})
    ]

    inlines = [ChoiceInLine]

    list_filter = ["pub_date"]
    search_fields = ["question_text"]

admin.site.register(Question, QuestionAdmin)
"""
