from django.db import models
from django.core.validators import MinValueValidator, \
                                   MaxValueValidator


class Coupon(models.Model):
    # код, который пользователи должны ввести, чтобы применить купон к своей покупке
    code = models.CharField(max_length=50,
                            unique=True)
    # значение даты/времени, указывающее, когда купон становится действительным
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    # применяемый уровень скидки
    discount = models.IntegerField(
                   validators=[MinValueValidator(0),
                               MaxValueValidator(100)],
                   help_text='Percentage vaule (0 to 100)')
    # является ли купон активным/неактивным
    active = models.BooleanField()

    def __str__(self):
        return self.code