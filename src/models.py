from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.username

class Purshare_types(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)

class Purchase(Model):
    id = fields.IntField(pk=True)
    buyer = fields.ForeignKeyField('models.User', related_name='buyer_purchases')
    seller = fields.ForeignKeyField('models.User', related_name='seller_purchases')
    purshare_type = fields.ForeignKeyField('models.Purshare_types')
    review = fields.CharField(max_length=900)
    sold_date = fields.DatetimeField()


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
