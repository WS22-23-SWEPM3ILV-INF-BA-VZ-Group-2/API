import uuid

from rest_framework import status
from rest_framework.test import APITestCase
from unreveal.models import User


class Login(APITestCase):
    def test_login(self):
        base_url = "http://127.0.0.1:8000/api"
        register_data = {
            "username": "benny22",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }
        self.client.post(f'{base_url}/user', register_data, format="json")

        data = {
            "email": "benny@gmail.com",
            "password": "unreveal"
        }
        response = self.client.post(f'{base_url}/login', data, format="json")

        self.assertEqual(
            response.content, b'{"message":"OK","description":"You are logged in"}')

    def test_login_multiple_users(self):
        base_url = "http://127.0.0.1:8000/api"
        register_data = {
            "username": "benny22",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }
        self.client.post(f'{base_url}/user', register_data, format="json")

        register_data = {
            "username": "tom",
            "email": "tom@gmail.com",
            "password": "unreveal"
        }
        self.client.post(f'{base_url}/user', register_data, format="json")

        data = {
            "email": "benny@gmail.com",
            "password": "unreveal"
        }
        response = self.client.post(f'{base_url}/login', data, format="json")

        data = {
            "email": "tom@gmail.com",
            "password": "unreveal"
        }
        response = self.client.post(f'{base_url}/login', data, format="json")

        self.assertEqual(
            response.content, b'{"message":"OK","description":"You are logged in"}')

    def test_login_user_not_found(self):
        url = "http://127.0.0.1:8000/api/login"

        data = {
            "email": "benny@gmail.com",
            "password": "unreveal"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_login_wrong_password(self):
        base_url = "http://127.0.0.1:8000/api"
        register_data = {
            "username": "benny22",
            "email": "benny@gmail.com",
            "password": "password"
        }
        self.client.post(f'{base_url}/user', register_data, format="json")

        data = {
            "email": "benny@gmail.com",
            "password": "unreveal"
        }
        response = self.client.post(f'{base_url}/login', data, format="json")

        self.assertEqual(
            response.content, b'{"error":"Bad Request","description":"email and password did not match"}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class Logout(APITestCase):
    def test_logout(self):
        base_url = "http://127.0.0.1:8000/api"
        register_data = {
            "username": "benny22",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }
        self.client.post(f'{base_url}/user', register_data, format="json")

        data = {
            "email": "benny@gmail.com",
            "password": "unreveal"
        }
        self.client.post(f'{base_url}/login', data, format="json")

        data = {
            "email": "benny@gmail.com",
        }

        response = self.client.post(f'{base_url}/logout', data, format='json')
        self.assertEqual(response.content, b'{"message":"OK","description":"You are logged out"}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_multiple_users(self):
        base_url = "http://127.0.0.1:8000/api"
        register_data = {
            "username": "benny22",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }
        self.client.post(f'{base_url}/user', register_data, format="json")

        register_data = {
            "username": "tom",
            "email": "tom@gmail.com",
            "password": "unreveal"
        }
        self.client.post(f'{base_url}/user', register_data, format="json")

        data = {
            "email": "benny@gmail.com",
            "password": "unreveal"
        }
        response = self.client.post(f'{base_url}/login', data, format="json")

        data = {
            "email": "tom@gmail.com",
            "password": "unreveal"
        }
        response = self.client.post(f'{base_url}/login', data, format="json")

        data = {
            "email": "benny@gmail.com",
        }

        response = self.client.post(f'{base_url}/logout', data, format='json')
        self.assertEqual(response.content, b'{"message":"OK","description":"You are logged out"}')

        data = {
            "email": "tom@gmail.com",
        }
        response = self.client.post(f'{base_url}/logout', data, format='json')
        self.assertEqual(response.content, b'{"message":"OK","description":"You are logged out"}')

    def test_fail_logout(self):
        url = "http://127.0.0.1:8000/api/logout"

        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.content,
                         b'{"error":"Bad Request","description":"invalid email"}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_without_login(self):
        url = "http://127.0.0.1:8000/api/logout"

        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.content,
                         b'{"error":"Bad Request","description":"invalid email"}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class Place(APITestCase):
    def test_create_place(self):
        base_url = "http://127.0.0.1:8000/api"
        data = {
            "username": "tom",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }

        self.client.post(f'{base_url}/user', data, format='json')

        data = {
            "email": "benny@gmail.com",
            "latitude": "1234657865",
            "longitude": "456786754",
            "name": "caffee",
            "description": "best caffee in berlin",
            "label": "caffe;relax;fun",
        }

        response = self.client.post(f'{base_url}/place', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_bad_request_create_place_user_do_not_exists(self):
        base_url = "http://127.0.0.1:8000/api"
        register_data = {
            "username": "benny22",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }
        self.client.post(f'{base_url}/user', register_data, format="json")

        data = {
            "email": "benny@gmail.com",
        }

        response = self.client.post(f'{base_url}/logout', data, format='json')
        self.assertEqual(response.content,
                         b'{"error":"Bad Request","description":"user is not logged in"}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_find_place(self):
        base_url = "http://127.0.0.1:8000/api"
        data = {
            "username": "tom",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }

        self.client.post(f'{base_url}/user', data, format='json')

        data = {
            "email": "benny@gmail.com",
            "latitude": "48.18765064595524",
            "longitude": "16.312395393454587",
            "name": "wien 2",
            "description": "best caffee in berlin",
            "label": "caffe;relax;fun",
        }
        
        response = self.client.post(f'{base_url}/place', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            "email": "benny@gmail.com",
            "latitude": "48.2121594130154",
            "longitude": "15.628637887792896",
            "name": "st. polten",
            "description": "best caffee in berlin",
            "label": "caffe;relax;fun",
        }
        
        response = self.client.post(f'{base_url}/place', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            "email": "benny@gmail.com",
            "latitude": "48.19158945620105",
            "longitude": "16.379863310872935",
            "name": "wien 1",
            "description": "best caffee in berlin",
            "label": "caffe;relax;fun",
        }

        response = self.client.post(f'{base_url}/place', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(
            f'{base_url}/place?latitude={response.data["latitude"]}&longitude={response.data["longitude"]}&range=10000', format='json')
        #range = 10000 = 10km
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("wien 1",response.content.decode("utf-8"))
        self.assertIn("wien 2",response.content.decode("utf-8"))


class CommentTest(APITestCase):
    def test_create_comment(self):
        base_url = "http://127.0.0.1:8000/api"
        data = {
            "username": "tom",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }

        self.client.post(f'{base_url}/user', data, format='json')

        data = {
            "email": "benny@gmail.com",
            "latitude": "1234657865",
            "longitude": "456786754",
            "name": "caffee",
            "description": "best caffee in berlin",
            "label": "caffe;relax;fun",
        }

        response = self.client.post(f'{base_url}/place', data, format='json')

        data = {
            "place_id": response.data['id'],
            "email": "benny@gmail.com",
            "comment": "Hi im here for testing",
        }

        response = self.client.post(f'{base_url}/comment', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_bad_request_create_comment_user_do_not_exists(self):
        base_url = "http://127.0.0.1:8000/api"

        data = {
            "username": "tom",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }

        self.client.post(f'{base_url}/user', data, format='json')

        data = {
            "email": "benny@gmail.com",
            "latitude": "1234657865",
            "longitude": "456786754",
            "name": "caffee",
            "description": "best caffee in berlin",
            "label": "caffe;relax;fun",
        }

        response = self.client.post(f'{base_url}/place', data, format='json')

        data = {
            "place_id": response.data['id'],
            "email": "marcus@gmail.com",
            "comment": "Hi im here for testing",
        }

        response = self.client.post(f'{base_url}/comment', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content,
                         b'{"error":"Not Found","description":"User matching query does not exist."}')

    def test_bad_request_create_comment_place_do_not_exists(self):
        base_url = "http://127.0.0.1:8000/api"

        data = {
            "username": "tom",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }

        self.client.post(f'{base_url}/user', data, format='json')

        data = {
            "place_id": uuid.uuid1(),
            "email": "benny@gmail.com",
            "comment": "Hi im here for testing",
        }

        response = self.client.post(f'{base_url}/comment', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content,
                         b'{"error":"Not Found","description":"Place matching query does not exist."}')

    def test_get_comment(self):
        base_url = "http://127.0.0.1:8000/api"
        data = {
            "username": "tom",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }

        self.client.post(f'{base_url}/user', data, format='json')

        data = {
            "email": "benny@gmail.com",
            "latitude": "1234657865",
            "longitude": "456786754",
            "name": "caffee",
            "description": "best caffee in berlin",
            "label": "caffe;relax;fun",
        }

        response = self.client.post(f'{base_url}/place', data, format='json')

        data = {
            "place_id": response.data['id'],
            "email": "benny@gmail.com",
            "comment": "Hi im here for testing",
        }

        self.client.post(f'{base_url}/comment', data, format='json')

        response = self.client.get(
            f'{base_url}/comment?place_id={response.data["id"]}', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_found_get_non_existent_comment(self):
        base_url = "http://127.0.0.1:8000/api"
        data = {
            "username": "tom",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }

        self.client.post(f'{base_url}/user', data, format='json')

        data = {
            "email": "benny@gmail.com",
            "latitude": "1234657865",
            "longitude": "456786754",
            "name": "caffee",
            "description": "best caffee in berlin",
            "label": "caffe;relax;fun",
        }

        response = self.client.post(f'{base_url}/place', data, format='json')

        response = self.client.get(
            f'{base_url}/comment?place_id={response.data["id"]}', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestUser(APITestCase):

    def test_user_not_found(self):
        url = "http://127.0.0.1:8000/api/user?username=tom"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_user(self):
        url = "http://127.0.0.1:8000/api/user"
        data = {
            "username": "tom",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(User.objects.filter(username='tom')), 1)

    def test_bad_request_create_user_wrong_email(self):
        url = "http://127.0.0.1:8000/api/user"
        data = {
            "username": "tom",
            "email": "bennygmail.com",
            "password": "unreveal"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user(self):
        url = "http://127.0.0.1:8000/api/user"
        data = {
            "username": "tom",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }
        self.client.post(url, data, format='json')
        response = self.client.get(f'{url}?email=benny@gmail.com', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_conflict_with_duplicated_user(self):
        url = "http://127.0.0.1:8000/api/user"
        data = {
            "username": "benny22",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }

        self.client.post(url, data, format='json')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


class RatingTest(APITestCase):
    def test_create_rating(self):
        base_url = "http://127.0.0.1:8000/api"
        data = {
            "username": "tom",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }

        self.client.post(f'{base_url}/user', data, format='json')

        data = {
            "email": "benny@gmail.com",
            "latitude": "1234657865",
            "longitude": "456786754",
            "name": "caffee",
            "description": "best caffee in berlin",
            "label": "caffe;relax;fun",
        }

        response = self.client.post(f'{base_url}/place', data, format='json')

        data = {
            "place_id": response.data['id'],
            "email": "benny@gmail.com",
            "rating":  4.5,
        }

        response = self.client.post(f'{base_url}/rating', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_bad_request_create_rating_user_do_not_exists(self):
        base_url = "http://127.0.0.1:8000/api"

        data = {
            "username": "tom",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }

        self.client.post(f'{base_url}/user', data, format='json')

        data = {
            "email": "benny@gmail.com",
            "latitude": "1234657865",
            "longitude": "456786754",
            "name": "caffee",
            "description": "best caffee in berlin",
            "label": "caffe;relax;fun",
        }

        response = self.client.post(f'{base_url}/place', data, format='json')

        data = {
            "place_id": response.data['id'],
            "email": "marcus@gmail.com",
            "rating": 2.5,
        }

        response = self.client.post(f'{base_url}/rating', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content,
                         b'{"error":"Not Found","description":"User matching query does not exist."}')

    def test_bad_request_create_rating_place_do_not_exists(self):
        base_url = "http://127.0.0.1:8000/api"

        data = {
            "username": "tom",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }

        self.client.post(f'{base_url}/user', data, format='json')

        data = {
            "place_id": uuid.uuid1(),
            "email": "benny@gmail.com",
            "rating": 2.8,
        }

        response = self.client.post(f'{base_url}/rating', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content,
                         b'{"error":"Not Found","description":"Place matching query does not exist."}')

    def test_get_rating(self):
        base_url = "http://127.0.0.1:8000/api"
        data = {
            "username": "tom",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }

        self.client.post(f'{base_url}/user', data, format='json')

        data = {
            "email": "benny@gmail.com",
            "latitude": "1234657865",
            "longitude": "456786754",
            "name": "caffee",
            "description": "best caffee in berlin",
            "label": "caffe;relax;fun",
        }

        response = self.client.post(f'{base_url}/place', data, format='json')

        data = {
            "place_id": response.data['id'],
            "email": "benny@gmail.com",
            "rating": 5,
        }

        self.client.post(f'{base_url}/rating', data, format='json')

        response = self.client.get(
            f'{base_url}/rating?place_id={response.data["id"]}', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_found_get_non_existent_rating(self):
        base_url = "http://127.0.0.1:8000/api"
        data = {
            "username": "tom",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }

        self.client.post(f'{base_url}/user', data, format='json')

        data = {
            "email": "benny@gmail.com",
            "latitude": "1234657865",
            "longitude": "456786754",
            "name": "caffee",
            "description": "best caffee in berlin",
            "label": "caffe;relax;fun",
        }

        response = self.client.post(f'{base_url}/place', data, format='json')

        response = self.client.get(
            f'{base_url}/rating?place_id={response.data["id"]}', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_bad_request_create_rating_above_five_belove_zero(self):
        base_url = "http://127.0.0.1:8000/api"

        data = {
            "username": "tom",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }

        self.client.post(f'{base_url}/user', data, format='json')

        data = {
            "place_id": uuid.uuid1(),
            "email": "benny@gmail.com",
            "rating": 8,
        }

        response = self.client.post(f'{base_url}/rating', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            "place_id": uuid.uuid1(),
            "email": "benny@gmail.com",
            "rating": -1,
        }

        response = self.client.post(f'{base_url}/rating', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
