from django.db import models



class Phone(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    image = models.URLField()
    release_date = models.DateField()
    lte_exists = models.BooleanField()
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return f'{self.name}, {self.price}: {self.release_date}'
