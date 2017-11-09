import json
import random

from flask import Response
from flask_restful_swagger_2 import Resource, swagger

from db.models.company import CompanyModel
from db.mongo_helper import mongo_to_dict

from routes.api import company_doc


class Company(Resource):
    uri = '/company'

    @swagger.doc(company_doc.COMPANY_GET)
    def get(self):
        company = random.choice(CompanyModel.objects)

        resp = mongo_to_dict(company, ['_cls'])

        if 'WantedModel' in str(company._cls):
            resp.update({
                'kind': 'wanted'
            })
        else:
            resp.update({
                'kind': 'rocketpunch'
            })

        return Response(json.dumps(resp, ensure_ascii=False), 200)
