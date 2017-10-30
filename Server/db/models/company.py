from db.mongo import *

WEB = 1
APP = 2
GAME = 3
SERVER = 4
SYSTEM = 5
SECURITY = 6


class CompanyModel(Document):
    title = StringField(required=True)
    address = StringField(required=True)
    logo = FileField()
    category = IntField(required=True)
