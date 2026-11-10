import unittest

from flask import json

from openapi_server.models.product_in import ProductIn  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_products_create_product(self):
        """Test case for products_create_product

        
        """
        product_in = {"name":"name","price":0.8008281904610115}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/products',
            method='POST',
            headers=headers,
            data=json.dumps(product_in),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_products_delete_product(self):
        """Test case for products_delete_product

        
        """
        headers = { 
        }
        response = self.client.open(
            '/products/{id}'.format(id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_products_get_product(self):
        """Test case for products_get_product

        
        """
        headers = { 
        }
        response = self.client.open(
            '/products/{id}'.format(id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_products_list_products(self):
        """Test case for products_list_products

        
        """
        headers = { 
        }
        response = self.client.open(
            '/products',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_products_update_product(self):
        """Test case for products_update_product

        
        """
        product_in = {"name":"name","price":0.8008281904610115}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/products/{id}'.format(id=56),
            method='PUT',
            headers=headers,
            data=json.dumps(product_in),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
