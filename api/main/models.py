"""
https://medium.com/geekculture/django-implementing-star-rating-e1deff03bb1c
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import send_activation_notification


class Photo(models.Model):
    author = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='photo_set')
    photo = models.ImageField(upload_to='photos/publications/%Y/%B')
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE, verbose_name='публикация', null=True)


class Publication(models.Model):
    slug = models.SlugField(verbose_name='Слаг', unique=True, db_index=True)
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    name = models.TextField(verbose_name='Название', max_length='170')
    description = models.TextField(verbose_name='Описание', max_length=500)
    is_active = models.BooleanField(verbose_name='Активен', default=True)
    price = models.FloatField(verbose_name='Цена в рублях')
    publication_date = models.DateField(verbose_name='дата публикации', auto_created=True)


    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'публикации'
        ordering = ['publication_date']


class Feedback(models.Model):
    class Marks(models.IntegerChoices):
        ONE = 1, '1'
        TWO = 2, '2'
        THREE = 3, '3'
        FOUR = 4, '4'
        FIVE = 5, '5'

    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='created_feedbacks', null=True)
    to = models.ForeignKey('User', on_delete=models.CASCADE, related_name='feedbacks', null=True)
    text = models.TextField(verbose_name='Текст', max_length=500, blank=True)
    mark = models.IntegerField(choices=Marks.choices, verbose_name='Оценка',)
    publication_date = models.DateField(verbose_name='дата публикации', auto_created=True,)


    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ['publication_date']
        

class User(AbstractUser):
    """
    Model for users
    Including fields: user_photo, is_seller, verified, rating, username, first_name, last_name, email, is_staff, is_active, date_joined,
    """
    # https://github.com/django/django/blob/main/django/contrib/auth/models.py    
    user_photo = models.ImageField(verbose_name='фото профиля', upload_to='photos/users/%Y/%B', null=True, blank=True)
    is_seller = models.BooleanField(default=False)
    verified = models.BooleanField(verbose_name='верификация', default=False)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ['date_joined']


@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
        if created:
            send_activation_notification(instance)