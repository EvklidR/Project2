from django.db import models


class Thing(models.Model):
    title = models.CharField('название', max_length=30)
    description = models.CharField('описание', max_length=50)
    inform = models.TextField('описание', max_length=2000)
    typeData = models.CharField('тип товара', max_length=50)
    date = models.DateTimeField('дата публикации', auto_now=True)
    cost = models.FloatField('цена')

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to='media')
    tov = models.ForeignKey(Thing, on_delete=models.CASCADE)

    def __str__(self):
        return self.image.url