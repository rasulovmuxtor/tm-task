import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

client = APIClient()


class ProductTest(APITestCase):
    fixtures = ['./warehouse/fixtures/dump.json', ]

    def setUp(self):
        self.products_payload = [
            {
                "product": 1,
                "quantity": 30
            },
            {
                "product": 2,
                "quantity": 20
            }
        ]

    def test_products_list(self):
        response = client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_materials_for_products(self):
        response = client.post(reverse('product-materials'),
                               data=json.dumps(self.products_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
