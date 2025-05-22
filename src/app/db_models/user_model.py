from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)  # ID (уникальный иднтификатор) пользователя в БД
    user_id = fields.IntField()  # ID пользователя в телеграм
    username = fields.CharField(50, null=True)  # Короткое имя пользователя
    name = fields.CharField(50)  # Имя пользователя в телеграме
    
    regdate = fields.DatetimeField(auto_now_add=True)  # *Дата регистрации

    class Meta:
        table = 'users'

    def __str__(self):
        return f'User(id={self.id}, user_id={self.user_id})'