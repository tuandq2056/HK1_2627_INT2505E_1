import flask
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.error_model import ErrorModel  # noqa: E501
from openapi_server.models.pet import Pet  # noqa: E501
from openapi_server.models.pet_base import PetBase  # noqa: E501
from openapi_server.models.pet_patch_request import PetPatchRequest  # noqa: E501
from openapi_server import util


def create_pet(body):  # noqa: E501
    """post new pet

     # noqa: E501

    :param pet_base: 
    :type pet_base: dict | bytes

    :rtype: Union[Pet, Tuple[Pet, int], Tuple[Pet, int, Dict[str, str]]
    """
    pet_base = body
    if flask.request.is_json:
        pet_base = PetBase.from_dict(flask.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_pet(pet_id):  # noqa: E501
    """delete pet

     # noqa: E501

    :param pet_id: ID
    :type pet_id: int

    :rtype: Union[Pet, Tuple[Pet, int], Tuple[Pet, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_pet_by_id(pet_id):  # noqa: E501
    """Check  only  a pet

     # noqa: E501

    :param pet_id: ID
    :type pet_id: int

    :rtype: Union[Pet, Tuple[Pet, int], Tuple[Pet, int, Dict[str, str]]
    """
    return 'do some magic!'


def list_pets(limit=None, status=None):  # noqa: E501
    """list pets

     # noqa: E501

    :param limit: LIMIT
    :type limit: int
    :param status: STATUS
    :type status: str

    :rtype: Union[List[Pet], Tuple[List[Pet], int], Tuple[List[Pet], int, Dict[str, str]]
    """
    return 'do some magic!'


def update_pet_partially(pet_id, body):  # noqa: E501
    """pathch pet

     # noqa: E501

    :param pet_id: ID
    :type pet_id: int
    :param pet_patch_request: 
    :type pet_patch_request: dict | bytes

    :rtype: Union[Pet, Tuple[Pet, int], Tuple[Pet, int, Dict[str, str]]
    """
    pet_patch_request = body
    if flask.request.is_json:
        pet_patch_request = PetPatchRequest.from_dict(flask.request.get_json())  # noqa: E501
    return 'do some magic!'
