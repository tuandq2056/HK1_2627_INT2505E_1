import flask
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.product_in import ProductIn  # noqa: E501
from openapi_server import util


def products_create_product(body):  # noqa: E501
    """products_create_product

     # noqa: E501

    :param product_in: 
    :type product_in: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    product_in = body
    if flask.request.is_json:
        product_in = ProductIn.from_dict(flask.request.get_json())  # noqa: E501
    return 'do some magic!'


def products_delete_product(id):  # noqa: E501
    """products_delete_product

     # noqa: E501

    :param id: 
    :type id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def products_get_product(id):  # noqa: E501
    """products_get_product

     # noqa: E501

    :param id: 
    :type id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def products_list_products():  # noqa: E501
    """products_list_products

     # noqa: E501


    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def products_update_product(id, body):  # noqa: E501
    """products_update_product

     # noqa: E501

    :param id: 
    :type id: int
    :param product_in: 
    :type product_in: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    product_in = body
    if flask.request.is_json:
        product_in = ProductIn.from_dict(flask.request.get_json())  # noqa: E501
    return 'do some magic!'
