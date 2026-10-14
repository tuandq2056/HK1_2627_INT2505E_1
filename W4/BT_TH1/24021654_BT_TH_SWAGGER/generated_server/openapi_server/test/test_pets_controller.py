import unittest

from flask import json

from openapi_server.models.error_model import ErrorModel  # noqa: E501
from openapi_server.models.pet import Pet  # noqa: E501
from openapi_server.models.pet_base import PetBase  # noqa: E501
from openapi_server.models.pet_patch_request import PetPatchRequest  # noqa: E501
from openapi_server.test import BaseTestCase


class TestPetsController(BaseTestCase):
    """PetsController integration test stubs"""

    def test_create_pet(self):
        """Test case for create_pet

        post new pet
        """
        pet_base = {"name":"Dodge","category":"Dodge","status":"available"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/pets',
            method='POST',
            headers=headers,
            data=json.dumps(pet_base),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_pet(self):
        """Test case for delete_pet

        delete pet
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/pets/{pet_id}'.format(pet_id=101),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_pet_by_id(self):
        """Test case for get_pet_by_id

        Check  only  a pet
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/pets/{pet_id}'.format(pet_id=101),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_pets(self):
        """Test case for list_pets

        list pets
        """
        query_string = [('limit', 20),
                        ('status', 'available')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/pets',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_pet_partially(self):
        """Test case for update_pet_partially

        pathch pet
        """
        pet_patch_request = {"name":"Dodge","status":"pending"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/pets/{pet_id}'.format(pet_id=101),
            method='PATCH',
            headers=headers,
            data=json.dumps(pet_patch_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
