from django.test import TestCase
from rest_framework.test import APIClient
from .models import Product


class ProductSoftDeleteTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.create(
            name='Test Product',
            sku='TST01',
            description='desc',
            shop='Shop',
            location='Loc',
            price=1000,
            discount=200,
            category='Cat',
            stock=10,
            is_available=True,
            picture='http://example.com/img.jpg'
        )

    def test_final_price(self):
        assert self.product.final_price() == 800

    def test_soft_delete_and_get(self):
        url = f'/products/{self.product.id}/'
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, 204)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data.get('is_delete'))
