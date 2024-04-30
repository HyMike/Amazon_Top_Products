from django.db import models

# Create your models here.


class Best_Sellers_List(models.Model):
    name = models.CharField(max_length=100)
    link = models.URLField()
    slug = models.SlugField(default='', null=True)

    # def __str__(self):
    #     return self.name
