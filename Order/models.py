from django.db import models


class OrderFile(models.Model):
    """Файлы приложенные к заказу"""
    file = models.FileField('Файл')
    name = models.CharField('Название файла', max_length=255)


class Stage(models.Model):
    """Стадия выполнения """
    name = models.CharField('Название задачи', max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=2,
                                verbose_name='Цена задачи', null=True)


class Order(models.Model):
    """Объект Заказа"""
    STATUS = (
        ('new', 'Новая'), # предложения принимаются
        ('offer_accepted', 'Предложение принято'),
        ('work', 'В работе'),
        ('complete', 'Выполнен'),
        ('crushed', 'Брошен')
        )
    client = models.ForeignKey('Manage.Person', on_delete=models.CASCADE)
    status = models.CharField('Статус', max_length=255, choices=STATUS,
                              default='new')
    name = models.CharField('Название', max_length=255)
    descr = models.TextField('Описание')
    rubric = models.ForeignKey('Manage.Rubric', on_delete=models.CASCADE)
    files = models.ManyToManyField(OrderFile, verbose_name='Прикреплённые файлы',
                                   blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2,
                                verbose_name='Итоговая Цена', null=True)
    # предложение работника которое в итог было принято
    result_offer = models.ForeignKey(
        'Order.Offer', null=True,
        on_delete=models.SET_NULL,
        related_name='res_offer',
        verbose_name='Принятое предложение'
    )
    add_time = models.DateTimeField('Время поступления', auto_now_add=True)
    stages = models.ManyToManyField(Stage, blank=True, related_name='all_stages')
    current_stage = models.ForeignKey(Stage, on_delete=models.SET_NULL,
                                      null=True, related_name='curr_stage')


class Offer(models.Model):
    """Предложение исполнителя на заказ"""
    OFTEN_PAY = (
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('full_pay', 'Полный объём'),
        # ('by_stage', 'Поэтапно')
        )
    worker = models.ForeignKey('Manage.Person', on_delete=models.CASCADE,
                                null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    header = models.CharField('Название/заголовок предложения', max_length=255)
    message = models.TextField('Сообщение заказчику')
    price = models.DecimalField(max_digits=20, decimal_places=2,
                                verbose_name='Предлженная цена')
    work_duration = models.DurationField('Срок выполнения')
    add_time = models.DateTimeField('Время поступления', auto_now_add=True)
    payment_mode = models.CharField('Режим оплаты', max_length=50,
                                    default='full_pay', choices=OFTEN_PAY)
