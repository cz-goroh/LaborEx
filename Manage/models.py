from django.db import models
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Rubric(models.Model):
    """Рубрики сервиса"""
    name = models.CharField('Название', max_length=255)
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL,
                                blank=True)
    is_top = models.BooleanField('Топовая рубрика', default=False)

    def __str__(self):
        return self.name


class Person(AbstractUser):
    """Расширенная модель пользователя"""
    POS =  (('admin', 'Админ'),('user', 'пользователь'))
    position = models.CharField('должность', max_length=255, choices=POS,
                                default='user')
    money =  models.DecimalField(max_digits=20, decimal_places=2,
                                    verbose_name="Личный счёт", default=0)
    tel = models.CharField('tel', max_length=255, null=True, blank=True)
    refer = models.ForeignKey("self", null=True, on_delete=models.SET_NULL,
                                blank=True)
    rubrics = models.ManyToManyField(Rubric, verbose_name='Рубрики исполнители')


class ReferalLink(models.Model):
    """реферальная ссылка может относиться как к приглашению в сервис,
    так и в проект"""
    code = models.CharField('Ссылка', max_length=255)
    parent = models.ForeignKey(Person, on_delete=models.CASCADE,
                                related_name='parent')
    child = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True,
                                related_name='child')
    # project


class Message(models.Model):
    """Сообщения в чате"""
    STATUS = (('new', 'Непрочитано'), ('read', 'Прочитано'))
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_to',
                                on_delete=models.CASCADE)
    status = models.CharField('Статус', max_length=10, choices=STATUS,
                              default='new')
    text = models.TextField('Текст', null=True, blank=True)
    sent_time = models.DateTimeField(auto_now_add=True)
    file = models.FileField('Файл', null=True, blank=True)
