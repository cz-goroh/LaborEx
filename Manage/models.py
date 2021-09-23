from django.db import models
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.models import AbstractUser

class Person(AbstractUser):
    """Расширенная модель пользователя"""
    POS =  (('admin', 'Админ'),('user', 'пользователь'))
    position = models.CharField('должность', max_length=255, choices=POS, default='user')
    money =  models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Личный счёт", default=0)
    tel = models.CharField('tel', max_length=255, null=True, blank=True)
