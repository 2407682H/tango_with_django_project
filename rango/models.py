import datetime

from django.db import models
from django.utils import timezone

#Category class
class Category(models.Model):
    name = models.CharField(max_length = 128, unique = True) #Define a character field of length 128 that must be unique
    views = models.IntegerField(default = 0)
    likes = models.IntegerField(default = 0)

    #Nested meta class to fix typo
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
      return self.name


#Page class
class Page(models.Model):
    category = models.ForeignKey(Category, on_delete = models.CASCADE) #Foreign key of category - OneToMany relationship
    title = models.CharField(max_length = 128)
    url = models.URLField()
    views = models.IntegerField(default = 0)

    def __str__(self):
        return self.title


"""
#Chapter 2 and 7 of Django tutorial
#Question class
class Question(models.Model):
    question_text = models.CharField(max_length = 200)
    pub_date = models.DateTimeField("Date published")

    def __str__(self):
        return self.question_text


    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days = 1)

    was_published_recently.admin_order_field = "pub_date"
    was_published_recently.boolean = True
    was_published_recently.short_description = "Published recently?"
#Choice class
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice_text = models.CharField(max_length = 200)
    votes = models.IntegerField(default = 0)

    def __str__(self):
        return self.choice_text
"""
