import pkgutil

from flask import Blueprint
from flask_restful_swagger_2 import Api

import config as cf


def _modules(package):
    modules = []

    def search(target):
        for loader, name, is_package in pkgutil.iter_modules(target.__path__):
            if is_package:
                search(loader.find_module(name).load_module(name))
            else:
                modules.append((loader, name))

    search(package)

    return modules


_global_resources = []


def _factory(package, endpoint, url_prefix='', api_spec_url='/api/swagger', api_ver=cf.API_VER, api_title=cf.API_TITLE, api_desc=cf.API_DESC):
    """
    :param package: Package for Auto Route
    :type package: package

    :param endpoint: Endpoint of Blueprint
    :type endpoint: str

    :param url_prefix: URL Prefix of Blueprint. default = ''
    :type url_prefix: str

    :param api_spec_url: Swagger API Spec URL. default ='/api/swagger'
    :type api_spec_url: str

    :param api_ver: Swagger API Version. default = config.API_VER
    :type api_ver: str

    :param api_title: Swagger API Title default = config.API_TITLE
    :type api_title: str

    :param api_desc: Swagger API Description. default = config.API_DESC
    :type api_desc: str

    :rtype: Blueprint
    """
    bp = Blueprint(endpoint, __name__, url_prefix=url_prefix)
    api = Api(bp, api_spec_url=api_spec_url, api_version=api_ver, title=api_title, description=api_desc)

    resources = set()

    for loader, name in _modules(package):
        module_ = loader.find_module(name).load_module(name)
        try:
            for resource in module_.Resource.__subclasses__():
                if resource not in _global_resources:
                    resources.add(resource)
                    _global_resources.append(resource)
        except AttributeError:
            pass

    for resource in resources:
        api.add_resource(resource, resource.uri)

    return bp

all_blueprints = ()
