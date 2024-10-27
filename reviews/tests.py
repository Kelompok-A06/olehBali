from django.test import TestCase
from django.urls import reverse
from catalog.models import Product
from .models import Reviews
from authentication.models import User

class ReviewViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="belajardjango", role="user")
        self.product = Product.objects.create(
            nama="Test Product",
            kategori="kerajinan_tangan",
            harga=10000,
            toko="Test Store",
            alamat="Test Address",
            deskripsi="Test Description"
        )
        self.client.login(username='testuser', password='belajardjango')

    def test_show_review(self):
        response = self.client.get(reverse('reviews:review', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product-review.html')
        self.assertContains(response, self.product.nama)

    def test_add_review_create(self):
        # Test creating a new review
        response = self.client.post(reverse('reviews:add_review', args=[self.product.id]), {
            'ratings': 5,
            'comments': 'Great product!',
        })
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Reviews.objects.count(), 1)
        self.assertEqual(Reviews.objects.first().comments, 'Great product!')

    def test_add_review_update(self):
        # Create a review to update
        review = Reviews.objects.create(
            ratings=4,
            comments='Good product',
            user=self.user,
            product=self.product
        )

        # Test updating the existing review
        response = self.client.post(reverse('reviews:add_review', args=[self.product.id]), {
            'ratings': 5,
            'comments': 'Updated comment',
            'review_id': review.id,
        })

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the review was updated in the database
        review.refresh_from_db()
        self.assertEqual(review.comments, 'Updated comment')
        self.assertEqual(review.ratings, 5)
        
    def test_delete_review(self):
        review = Reviews.objects.create(
            user=self.user,
            product=self.product,
            ratings=5,
            comments='Great product!'
        )
        response = self.client.post(reverse('reviews:delete_review', args=[review.id]))
        self.assertFalse(Reviews.objects.filter(id=review.id).exists())

    def test_review_json_all(self):
        response = self.client.get(reverse('reviews:review_json_all'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, '[]') 
    
    def test_review_json_all_2(self):
        review = Reviews.objects.create(
            user=self.user,
            product=self.product,
            ratings=5,
            comments='Great product!'
        )
        
        response = self.client.get(reverse('reviews:review_json_all'))
        self.assertEqual(response.status_code, 200)

        expected_response = [
            {
                "model": "reviews.reviews",
                "pk": review.id,
                "fields": {
                    "user": self.user.id,  
                    "product": self.product.id,
                    "ratings": review.ratings,
                    "comments": review.comments,
                }
            }
        ]
        self.assertJSONEqual(response.content, expected_response)

    def test_review_json(self):
        review = Reviews.objects.create(
            user=self.user,
            product=self.product,
            ratings=5,
            comments='Great product!'
        )

        response = self.client.get(reverse('reviews:review_json', args=[self.product.id]))
        expected_response = [{
            'id': review.pk,
            'ratings': review.ratings,
            'comments': review.comments,
            'username': review.user.username,
        }]

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, expected_response)


    def test_chosen_review_json(self):
        review = Reviews.objects.create(
            user=self.user,
            product=self.product,
            ratings=5,
            comments='Great product!'
        )

        response = self.client.get(reverse('reviews:chosen_review_json', args=[review.id]))
        self.assertEqual(response.status_code, 200)

        expected_response = [
            {
                "model": "reviews.reviews",
                "pk": review.id,
                "fields": {
                    "user": self.user.id,
                    "product": self.product.id,
                    "ratings": review.ratings,
                    "comments": review.comments,
                }
            }
        ]
        self.assertJSONEqual(response.content, expected_response)