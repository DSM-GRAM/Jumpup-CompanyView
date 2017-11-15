from db.mongo import db


class CompanyModel(db.Document):
    name = db.StringField(required=True)
    image_url = db.StringField()
    logo_url = db.StringField()

    info = db.StringField()

    establish = db.StringField()
    member_count = db.StringField()
    address = db.StringField()

    meta = {'allow_inheritance': True}


class WantedModel(CompanyModel):
    label = db.StringField()
    positions = db.ListField(db.StringField())


class PositionEmbeddedModel(db.EmbeddedDocument):
    position_name = db.StringField()
    position_info = db.StringField()
    tech_stack = db.StringField()


class RocketPunchModel(CompanyModel):
    # email = StringField()
    tags = db.ListField(db.StringField())
    positions = db.ListField(db.EmbeddedDocumentField(PositionEmbeddedModel))
