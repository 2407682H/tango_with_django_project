from django.db import models
from django.template.defaultfilters import slugify


class Category(models.Model):   # Category class
    name = models.CharField(max_length = 128, unique = True)
    views = models.IntegerField(default = 0)
    likes = models.IntegerField(default = 0)
    slug = models.SlugField(unique = True)

    class Meta:     # Nested meta class to fix typo
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Page(models.Model):   # Page class
    category = models.ForeignKey(Category, on_delete = models.CASCADE) #Foreign key of category - OneToMany relationship
    title = models.CharField(max_length = 128)
    url = models.URLField()
    views = models.IntegerField(default = 0)

    def __str__(self):
        return self.title