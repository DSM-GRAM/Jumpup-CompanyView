from db.mongo import *


class CompanyModel(Document):
    name = StringField(required=True)
    image_url = StringField()
    logo_url = StringField()

    info = StringField()

    establish = StringField()
    member_count = StringField()
    address = StringField(required=True)

    meta = {'allow_inheritance': True}


class WantedModel(CompanyModel):
    label = StringField()
    positions = ListField(StringField())


class PositionEmbeddedModel(EmbeddedDocument):
    position_name = StringField()
    position_info = StringField()
    tech_stack = StringField()


class RocketPunchModel(CompanyModel):
    email = StringField()
    tags = ListField(StringField())
    positions = ListField(EmbeddedDocumentField(PositionEmbeddedModel))
