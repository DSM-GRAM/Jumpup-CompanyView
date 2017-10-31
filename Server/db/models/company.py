from db.mongo import *


class CompanyModel(Document):
    company_name = StringField(required=True)
    address = StringField(required=True)
    company_intro = StringField()
    background_image = FileField()
    logo = FileField()

    establish = StringField()
    member_count = StringField()

    meta = {'allow_inheritance': True}


class WantedModel(CompanyModel):
    company_position = StringField()
    positions = ListField(StringField())


class PositionEmbeddedModel(EmbeddedDocument):
    position_name = StringField()
    position_info = StringField()
    tech_stack = StringField()


class RocketPunchModel(CompanyModel):
    email = StringField()
    tags = ListField(StringField())
    positions = ListField(EmbeddedDocumentField(PositionEmbeddedModel))
