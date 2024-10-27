from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product
from .forms import ProductForm

class CatalogTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.product = Product.objects.create(
            nama='Test Product',
            kategori='makanan_minuman',
            harga=10000,
            toko='Test Toko',
            alamat='Test Alamat',
            deskripsi='Test Deskripsi'
        )

    def test_catalog_url_exists(self):
        response = self.client.get(reverse('catalog:catalog'))
        self.assertEqual(response.status_code, 200)

    def test_add_product_url_exists(self):
        response = self.client.get(reverse('catalog:add_product'))
        self.assertEqual(response.status_code, 200)

    def test_add_product_form_submission(self):
        form_data = {
            'nama': 'New Product',
            'kategori': 'pakaian',
            'harga': 20000,
            'alamat': 'New Alamat',
            'deskripsi': 'New Deskripsi',
        }
        response = self.client.post(reverse('catalog:add_product'), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Product.objects.filter(nama='New Product').exists())

    def test_delete_product(self):
        response = self.client.post(reverse('catalog:delete_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_search_functionality(self):
        response = self.client.get(reverse('catalog:catalog') + '?search=Test')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

    def test_pagination(self):
        for i in range(15):  # Add extra products to test pagination
            Product.objects.create(
                nama=f'Product {i}',
                kategori='makanan_minuman',
                harga=10000,
                toko='Test Toko',
                alamat='Test Alamat',
                deskripsi='Test Deskripsi'
            )
        response = self.client.get(reverse('catalog:catalog'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 14)

    def test_product_form_invalid(self):
        form_data = {
            'nama': '',
            'kategori': 'makanan_minuman',
            'harga': -10000,
            'alamat': '',
            'deskripsi': 'Invalid Product',
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())

