from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

from django.contrib.auth.models import PermissionsMixin
from django.db import models


class MessageManager(models.Manager):
    def create_message(self, content):
        message = self.create(content=content)
        return message


class Message(models.Model):
    content = models.CharField(max_length=255)
    objects = MessageManager()

    def __str__(self):
        return 'Сообщение номер: ' + str(self.pk)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['content']


class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class TeamLeader(models.Model):
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Тим-лидер'
        verbose_name_plural = 'Тим-лидеры'
        ordering = ['username']


class Office(models.Model):
    location = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.location

    class Meta:
        verbose_name = 'Офис'
        verbose_name_plural = 'Офисы'


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    team_leader = models.ForeignKey(TeamLeader, related_name='team_lead',on_delete=models.CASCADE,null=True)
    is_staff = models.BooleanField(default=False)
    job_title = models.CharField(max_length=255)
    office = models.ManyToManyField(Office)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']
