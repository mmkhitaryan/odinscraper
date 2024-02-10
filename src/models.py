from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.username


class UserDetail(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User')
    last_login = fields.DatetimeField()
    last_register_date = fields.DatetimeField()
    tatal_sales = fields.IntField()
    total_sold_items = fields.IntField()
    int_rating = fields.IntField()

    def __str__(self):
        return self.username

class Shell(Model):
    id = fields.IntField(pk=True)
    machine_hostname = fields.CharField(max_length=255)
    country = fields.CharField(max_length=255)
    http_type = fields.CharField(max_length=255)
    tld = fields.CharField(max_length=255)
    masked_domain = fields.CharField(max_length=255)
    isp = fields.CharField(max_length=255)
    seo = fields.CharField(max_length=255)

    price = fields.FloatField()
    post_date = fields.DatetimeField()
    created_at = fields.DatetimeField(auto_now_add=True)

    user = fields.ForeignKeyField('models.User')

    def __str__(self):
        return self.id

class Cpanel(Model):
    id = fields.IntField(pk=True)
    country = fields.CharField(max_length=255)
    http_type = fields.CharField(max_length=255)
    tld = fields.CharField(max_length=255)
    masked_domain = fields.CharField(max_length=255)
    cms = fields.CharField(max_length=255)
    isp = fields.CharField(max_length=255)

    price = fields.FloatField()
    created_at = fields.DatetimeField(auto_now_add=True)

    user = fields.ForeignKeyField('models.User')

    def __str__(self):
        return self.id
