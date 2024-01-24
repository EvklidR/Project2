from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from main.models import Thing

class User(AbstractUser):
    email = models.EmailField(unique=True)
    tovars_c = models.ManyToManyField(Thing, through='My_card', related_name='basket')
    tovars_b = models.ManyToManyField(Thing, through='My_buyes')
    def get_absolute_url(self):
        return f'/au/{self.id}'


class My_card(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    tov = models.ForeignKey(Thing, on_delete=models.CASCADE)
    amount = models.IntegerField()

class My_crcard(models.Model):
    numb = models.CharField(max_length=16)
    srok = models.CharField(max_length=5)
    three = models.CharField(max_length=3)
    summa = models.FloatField(default=2000)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.numb[:4] + '*'*8 + self.numb[-4:]


class My_buyes(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    tov = models.ForeignKey(Thing, on_delete=models.CASCADE)
    card = models.ForeignKey(My_crcard, on_delete=models.CASCADE)
    adress = models.CharField(max_length=100)
    dateBuy = models.DateTimeField(auto_now=True)
